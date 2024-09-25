from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password"})
    )

    is_company = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label="Are you a company?",
        required=False,
    )

    class Meta:
        model = UserModel
        fields = (
            "email",
            "is_company",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserModel.objects.filter(email=email).exists():
            raise ValidationError("Email already in use. Try use another email")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"].split("@")[0]
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ("email", "is_company")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Enter your new email"}),
            "is_company": forms.CheckboxInput(
                attrs={"placeholder": "Are you a company?"}
            ),
        }


from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

UserModel = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"autofocus": True, "placeholder": "Enter your email"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"})
    )
    remember_me = forms.BooleanField(
        required=False, initial=False, widget=forms.CheckboxInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
