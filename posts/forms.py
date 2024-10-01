from django import forms
from django_select2.forms import Select2MultipleWidget, Select2Widget
from core.choices_utils import WORKPLACE_TYPES, WORK_TYPES
from .models import JobPost
from core.models import Country


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = (
            "title",
            "description",
            "country",
            "skills_required",
            "workplace_type",
            "work_type",
            "start_salary",
            "end_salary",
            "currency",
        )
        widgets = {
            'skills_required': Select2MultipleWidget,
            'country': Select2Widget,
        }


class FilterJobsForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Country.objects.all(),
                                      widget=Select2Widget(attrs={'class': 'form-select'}), required=False,
                                      label="Location", label_suffix="")
    workplace_type = forms.ChoiceField(choices=[("", "")] + WORKPLACE_TYPES,
                                       widget=forms.Select(attrs={'class': 'form-select', }), required=False,
                                       label="Workplace Type", label_suffix="")
    work_type = forms.ChoiceField(choices=[("", "")] + WORK_TYPES, widget=forms.Select(attrs={'class': 'form-select'}),
                                  required=False, label="Work Type", label_suffix="")
