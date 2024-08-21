from django.urls import path
from views import (
    JobListView,
    JobDetailView,
    JobCreateView,
    JobUpdateView,
    JobDeleteView,
    CompanyDetailView,
)

urlpatterns = [
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    path("jobs/<int:pk>/edit/", JobUpdateView.as_view(), name="job_edit"),
    path("jobs/<int:pk>/delete/", JobDetailView.as_view(), name="job_delete"),
    path("jobs/new/", JobCreateView.as_view(), name="job_add"),
    path("jobs/", JobListView.as_view(), name="job_list"),
    path(
        "companies/<slug:company>/", CompanyDetailView.as_view(), name="company_detail"
    ),
    path("skills/<slug:skill>/", CompanyDetailView.as_view(), name="skill_detail"),
    path(
        "industries/<slug:industry>/",
        CompanyDetailView.as_view(),
        name="industry_detail",
    ),
]
