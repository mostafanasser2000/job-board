from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["cover_letter", "resume"]
        widgets = {
            "cover_letter": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Write your cover letter"}
            )
        }

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")
        if resume and resume.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Resume file size should be 5MB or less")
        return resume
