from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import redirect


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
            return redirect(reverse("accounts:login"))

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
    
class CustomLoginView(LoginView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard:index'))
        return super().dispatch(request, *args, **kwargs)