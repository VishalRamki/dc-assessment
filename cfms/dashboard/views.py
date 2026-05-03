from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import redirect

from .forms import NoteForm

from .models import Complaint, ComplaintStatus


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "complaint/index.html"
    context_object_name = "latest_complaints_list"

    def get_queryset(self):
        user = self.request.user

        qs = Complaint.objects.order_by("-sub_date")

        if user.is_staff or user.is_superuser:
            return qs

        if user.groups.filter(name="Agent").exists():
            return qs.filter(assigned_agent_ref=user)

        return qs.filter(customer_account_ref=user)


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Complaint
    template_name = "complaint/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # only allow certain group (e.g. "Agent")
        if user.groups.filter(name="Agent").exists() or user.groups.filter(name="Admin"):
            context["note_form"] = NoteForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        user = request.user

        # block if not in group
        if not user.groups.filter(name="Agent").exists() and not user.groups.filter(name="Admin").exists():
            return redirect("dashboard:detail", pk=self.object.pk)

        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = user
            note.save()

            # attach note to complaint
            self.object.notes.add(note)

        return redirect("dashboard:detail", pk=self.object.pk)


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