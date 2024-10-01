from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .models import (
    UserProfile,
    CompanyProfile,
    Education,
    UserSkill,
    Experience,
)


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = [
            "user",
        ]
        widgets = {
            "country": Select2Widget,
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ["user", "slug"]

        widgets = {
            "country": Select2Widget,
            "industries": Select2MultipleWidget,
            "founded_at": forms.DateInput(attrs={"type": "date"}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = [
            "user",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = [
            "user",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class UserSkillsForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        exclude = [
            "user",
        ]
        widgets = {"skill": Select2Widget}
