from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.http import HttpRequest
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse


class SignUpView(CreateView):
    model = CustomUser
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = CustomAuthenticationForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return self.redirect_authenticated_user()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")

        if not remember_me:
            self.request.session.set_expiry(0)

        response = super().form_valid(form)
        user = form.get_user()

        if user.last_login is None:
            return self.redirect_first_time_login(user)

        return response

    def redirect_authenticated_user(self):
        next_url = self.request.GET.get("next") or self.get_success_url()
        return redirect(next_url)

    def redirect_first_time_login(self, user):
        if user.is_company:
            return redirect(
                reverse("company_profile", kwargs={"username": user.username})
            )
        return redirect(reverse("user_profile", kwargs={"username": user.username}))


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("job_list")
