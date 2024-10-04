from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("applicant", "job_post", "status", "created")
    list_filter = ("status", "created", "job_post")
    search_fields = ("applicant__username", "job_post__title")
    readonly_fields = ("created", "updated")
    actions = ["marked_as_reviewed", "marked_as_selected", "marked_as_rejected"]

    def marked_as_reviewed(self, request, queryset):
        queryset.update(status="reviewed")

    marked_as_reviewed.short_description = "Mark selected applications as reviewed"

    def marked_as_selected(self, request, queryset):
        queryset.update(status="selected")

    marked_as_selected.short_description = (
        "Mark selected applications as selected for next phase"
    )

    def marked_as_rejected(self, request, queryset):
        queryset.update(status="rejected")

    marked_as_rejected.short_description = "Mark selected applications as rejected"
