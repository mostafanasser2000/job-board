from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.edit import CreateView


class SignUpView(CreateView):
    model = CustomUser
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = "login"


def logout_view(request):
    logout(request)
    return redirect("job_list")
