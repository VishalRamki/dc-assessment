from datetime import timedelta

from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import redirect
from django.db.models import F, Avg, Count, DurationField, ExpressionWrapper

from dashboard.models import Complaint, ComplaintStatus
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "summary/index.html"
    context_object_name = "latest_complaints_list"

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        # redirect customers away
        if not (
            user.is_staff
            or user.is_superuser
            or user.groups.filter(name="Admin").exists()
            or user.groups.filter(name="Agent").exists()
        ):
            return redirect(reverse('dashboard:index'))

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        qs = Complaint.objects.order_by("-sub_date")

        if user.is_staff or user.is_superuser or user.groups.filter(name="Admin").exists():
            return qs

        if user.groups.filter(name="Agent").exists():
            return qs.filter(assigned_agent_ref=user)

        # this is the customer view ; just redirect to the complaint section
        return qs.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = context["latest_complaints_list"]

        context["total_count"] = qs.count()
        context["open_count"] = qs.filter(complaint_status_ref__name="Open").count()
        context["resolved_count"] = qs.filter(complaint_status_ref__name="Resolved").count()

        context["category_counts"] = (
            qs.values("complaint_category_ref__name")
              .annotate(count=Count("id"))
              .order_by("-count")
        )

        context["status_counts"] = (
            qs.values("complaint_status_ref__name")
              .annotate(count=Count("id"))
              .order_by("-count")
        )

        resolved_qs = qs.filter(complaint_status_ref__name="Resolved")

        context["avg_resolution_time"] = resolved_qs.aggregate(
            avg_time=Avg(
                ExpressionWrapper(
                    F("last_update_date") - F("sub_date"),
                    output_field=DurationField()
                )
            )
        )["avg_time"]

        avg_time = context["avg_resolution_time"]

        if avg_time:
            total_seconds = int(avg_time.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            context["avg_resolution_display"] = f"{hours}h {minutes}m"
        else:
            context["avg_resolution_display"] = "N/A"


        SLA_DAYS = 5

        threshold_date = timezone.now() - timedelta(days=SLA_DAYS)

        context["sla_breaches"] = qs.filter(
            sub_date__lt=threshold_date
        ).exclude(
            complaint_status_ref__name="Closed"
        )

        context["sla_breach_count"] = context["sla_breaches"].count()


        return context
    
class CustomLoginView(LoginView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard:index'))
        return super().dispatch(request, *args, **kwargs)