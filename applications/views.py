from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ApplicationForm
from .models import Application
from posts.models import JobPost
from django.urls import reverse
from django.contrib import messages


@require_POST
@login_required
def apply_for_job(request, slug):
    print("Applying for job:", slug)  # Debug statement
    job = get_object_or_404(JobPost, slug=slug, status="opened")
    if not request.user.is_company:
        if Application.objects.filter(applicant=request.user, job_post=job).exists():
            return redirect(
                "application_detail", job_slug=job.slug, username=request.user.username
            )

        form = ApplicationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.job_post = job
            application.save()

            return redirect(
                "application_detail", job_slug=job.slug, username=request.user.username
            )
        else:
            print(form.errors)
    return redirect(
        "job_detail",
        slug=slug,
    )


@login_required
def application_detail(request, job_slug, username):
    application = get_object_or_404(
        Application, job_post__slug=job_slug, applicant__username=username
    )
    if (
        application.applicant != request.user
        and application.job_post.publisher != request.user
    ):
        return redirect("job_list")

    is_owner = application.applicant == request.user
    return render(
        request,
        "applications/detail.html",
        {"application": application, "is_owner": is_owner},
    )


@login_required
def get_user_applications(request):
    if request.user.is_company:
        return redirect("job_list")
    applications = Application.objects.filter(applicant=request.user).select_related(
        "job_post"
    )
    pending_count = applications.filter(status="pending").count()
    selected_count = applications.filter(status="selected").count()
    rejected_count = applications.filter(status="rejected").count()
    context = {
        "applications": applications,
        "pending_count": pending_count,
        "selected_count": selected_count,
        "rejected_count": rejected_count,
    }

    return render(request, "applications/user.html", context)


@login_required
def get_job_applications(request, job_slug):
    job = get_object_or_404(JobPost, slug=job_slug)
    if job.publisher != request.user:
        return redirect("job_list")

    applications = job.applications.select_related("applicant")
    pending_count = applications.filter(status="pending").count()
    selected_count = applications.filter(status="selected").count()
    rejected_count = applications.filter(status="rejected").count()
    context = {
        "applications": applications,
        "job": job,
        "pending_count": pending_count,
        "selected_count": selected_count,
        "rejected_count": rejected_count,
    }

    return render(
        request,
        "applications/job.html",
        context,
    )


@require_POST
@login_required
def update_application_status(request, job_slug, username):
    application = application = get_object_or_404(
        Application,
        job_post__publisher=request.user,
        job_post__slug=job_slug,
        applicant__username=username,
    )
    status = request.POST.get("status", "")
    if status in ["selected", "rejected"]:
        application.status = status
        application.save()
    return redirect("application_detail", job_slug=job_slug, username=username)
