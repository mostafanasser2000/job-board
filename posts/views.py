from accounts.permissions import CompanyRequiredMixin, OwnerRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import JobPostForm
from .models import JobPost
from .forms import FilterJobsForm
from django.db.models import Q
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from profiles.models import CompanyProfile
from django.db.models import Avg
from applications.models import Application
from applications.forms import ApplicationForm


class JobPostListView(ListView):
    model = JobPost
    context_object_name = "jobs"
    paginate_by = 10

    def get_queryset(self):
        query_set = JobPost.objects.select_related("publisher", "country").filter(
            status="opened"
        )
        filters = Q()
        if self.request.GET.get("q"):
            q = self.request.GET.get("q")
            filters &= Q(title__icontains=q) | Q(description__icontains=q)
        if self.request.GET.get("location"):
            location = self.request.GET.get("location")
            filters &= Q(country__id=location)
        if self.request.GET.get("workplace_type"):
            workplace_type = self.request.GET.get("workplace_type")
            filters &= Q(workplace_type=workplace_type)
        if self.request.GET.get("work_type"):
            work_type = self.request.GET.get("work_type")
            filters &= Q(work_type=work_type)
        if self.request.GET.get("skills"):
            skills = self.request.GET.getlist("skills")
            filters &= Q(skills_required__slug__in=skills)
        return query_set.filter(filters).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = FilterJobsForm()
        return context


class JobPostDetailView(DetailView):
    model = JobPost
    context_object_name = "job"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and not self.request.user.is_company:
            if Application.objects.filter(
                job_post=self.get_object(), applicant=self.request.user
            ).exists():
                context["is_applied"] = True
            else:
                form = ApplicationForm()
                context["form"] = form
        context["full_url"] = self.request.build_absolute_uri(self.get_object().get_absolute_url())
        
        return context


class JobPostCreateView(LoginRequiredMixin, CompanyRequiredMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    success_url = reverse_lazy("job_list")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.publisher = self.request.user
        return super().form_valid(form)


class JobPostUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = JobPost
    form_class = JobPostForm


class JobPostDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = JobPost
    success_url = reverse_lazy("job_list")


@login_required
def dashboard(request):
    jobs = JobPost.objects.select_related("publisher", "country").filter(
        publisher=request.user
    )

    company = get_object_or_404(
        CompanyProfile.objects.values("name", "user"), user=request.user.id
    )
    open_jobs = JobPost.objects.filter(publisher=request.user, status="opened").count()
    total_applicants = Application.objects.filter(
        job_post__publisher=request.user
    ).count()
    context = {
        "jobs": jobs,
        "company": company,
        "open_jobs": open_jobs,
        "total_applicants": total_applicants,
    }
    return render(request, "dashboard.html", context)


@login_required
def open_job(request, slug):
    job = get_object_or_404(JobPost, slug=slug, publisher=request.user)
    job.status = "opened"
    job.save()
    return redirect("dashboard")


@login_required
def close_job(request, slug):
    job = get_object_or_404(JobPost, slug=slug, publisher=request.user)
    job.status = "closed"
    job.save()
    return redirect("dashboard")
