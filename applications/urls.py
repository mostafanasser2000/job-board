from django.urls import path
from . import views

urlpatterns = [
    path("job/<slug:job_slug>/", views.get_job_applications, name="job_applications"),
    path("apply/<slug:slug>/", views.apply_for_job, name="job_apply"),
    path(
        "<slug:job_slug>/<str:username>/update_status/",
        views.update_application_status,
        name="application_update",
    ),
    path(
        "<slug:job_slug>/<str:username>/",
        views.application_detail,
        name="application_detail",
    ),
    path("user/", views.get_user_applications, name="user_applications"),
]
