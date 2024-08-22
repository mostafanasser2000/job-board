from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Job


class JobListView(ListView):
    model = Job
    context_object_name = "jobs"


class JobDetailView(DetailView):
    model = Job


class JobCreateView(CreateView):
    model = Job
    fields = (
        "title",
        "company",
        "description",
        "skills_required",
        "workplace_type",
        "work_type",
        "salary_lowest",
        "salary_highest",
        "salary_currency",
        "apply_link",
    )


class JobUpdateView(UpdateView):
    model = Job
    fields = (
        "title",
        "description",
        "skills_required",
        "workplace_type",
        "work_type",
        "salary_lowest",
        "salary_highest",
        "salary_currency",
        "apply_link",
    )


class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy("job_list")


class CompanyDetailView(DetailView):
    pass
