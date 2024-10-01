from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("select2/", include("django_select2.urls")),
    path("jobs/", include("posts.urls")),
    path("", include("profiles.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [path("", RedirectView.as_view(url="jobs/", permanent=True))]
