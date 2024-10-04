from django.urls import path
from . import views

urlpatterns = [
    path("filter/", views.JobPostListView.as_view(), name="jobs_filter"),
    path("search/", views.JobPostListView.as_view(), name="jobs_search"),
    path("new/", views.JobPostCreateView.as_view(), name="job_add"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("<slug:slug>/", views.JobPostDetailView.as_view(), name="job_detail"),
    path("<slug:slug>/edit/", views.JobPostUpdateView.as_view(), name="job_edit"),
    path("<slug:slug>/delete/", views.JobPostDeleteView.as_view(), name="job_delete"),
    path("<slug:slug>/close/", views.close_job, name="job_close"),
    path("<slug:slug>/open/", views.open_job, name="job_open"),
    path("", views.JobPostListView.as_view(), name="job_list"),
]
