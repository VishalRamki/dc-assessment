from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Complaint


class IndexView(generic.ListView):
    template_name = "complaint/index.html"
    context_object_name = "latest_complaints_list"

    def get_queryset(self):
        return Complaint.objects.order_by("-sub_date")


class DetailView(generic.DetailView):
    model = Complaint
    template_name = "complaint/detail.html"


class ResultsView(generic.DetailView):
    model = Complaint