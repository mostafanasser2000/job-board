from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email", "is_superuser", "is_company"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_company",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("is_company",),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
