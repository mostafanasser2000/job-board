from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    is_company = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label="Are You Creating This Account For Posting Jobs?",
        required=False,
    )

    class Meta:
        model = UserModel
        fields = UserCreationForm.Meta.fields + (
            "email",
            "is_company",
        )

    def clean_email(self):
        data = self.changed_data["email"]
        if UserModel.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in user.")
        return data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = UserCreationForm.Meta.fields + ("is_company",)
