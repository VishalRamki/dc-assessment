from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .models import Complaint, ComplaintStatus


class IndexView(generic.ListView):
    template_name = "complaint/index.html"
    context_object_name = "latest_complaints_list"

    def get_queryset(self):
        return Complaint.objects.order_by("-sub_date")


class DetailView(generic.DetailView):
    model = Complaint
    template_name = "complaint/detail.html"

class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Complaint
    template_name = "complaint/create.html"
    fields = ["description", "complaint_category_ref"]  # keep it simple

    def form_valid(self, form):
        # set the logged-in user as the customer
        form.instance.customer_account_ref = self.request.user

        # set timestamps
        form.instance.sub_date = timezone.now()
        form.instance.last_update_date = timezone.now()

        # optionally assign an agent (simple example)
        # form.instance.assigned_agent_ref = User.objects.filter(is_staff=True).first()
        form.instance.complaint_status_ref = ComplaintStatus.objects.get(name="Open")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("dashboard:detail", kwargs={"pk": self.object.pk})

class ResultsView(generic.DetailView):
    model = Complaint