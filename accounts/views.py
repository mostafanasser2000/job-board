from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .models import CustomUser

class SignUpView(CreateView):
    model = CustomUser
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = "login"
