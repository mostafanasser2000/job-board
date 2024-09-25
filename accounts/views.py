from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.http import HttpRequest
from django.contrib.auth.views import LoginView


class SignUpView(CreateView):
    model = CustomUser
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = "login"


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = CustomAuthenticationForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            next_url = self.request.GET.get("next") or self.get_success_url()
            return redirect(next_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("job_list")
