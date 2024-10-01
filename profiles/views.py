from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.db.models import Prefetch
from posts.models import JobPost

from accounts.permissions import OwnerRequiredMixin, UserRequiredMixin
from .forms import (
    UserProfileForm,
    CompanyProfileForm,
    EducationForm,
    ExperienceForm,
    UserSkillsForm,
)
from .models import (
    UserProfile,
    CompanyProfile,
    Education,
    Experience,
    UserSkill,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["educations"] = Education.objects.filter(user=self.object.user)
        context["experiences"] = Experience.objects.filter(user=self.object.user)
        context["skills"] = UserSkill.objects.filter(user=self.object.user)
        context["is_owner"] = (
            self.request.user.is_authenticated and self.request.user == self.object.user
        )
        return context


class CompanyProfileMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["open_jobs"] = JobPost.objects.opened.filter(
            publisher=self.object.user
        )[:5]
        return context


class UserProfileDetailView(UserProfileMixin, DetailView):
    model = UserProfile
    template_name = "user/profile.html"
    context_object_name = "profile"

    def get_object(self):
        return get_object_or_404(UserProfile, user__username=self.kwargs["username"])


class UserProfileUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = UserProfile
    template_name = "user/form.html"
    form_class = UserProfileForm
    context_object_name = "profile"

    def get_object(self):
        return get_object_or_404(UserProfile, user__username=self.kwargs["username"])


class CompanyProfileDetailView(CompanyProfileMixin, DetailView):
    model = CompanyProfile
    template_name = "company/profile.html"
    context_object_name = "company"

    def get_object(self):
        return get_object_or_404(
            CompanyProfile.objects.select_related("user", "country").prefetch_related(
                "industries"
            ),
            user__username=self.kwargs["username"],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = (
            self.request.user.is_authenticated and self.object.user == self.request.user
        )
        return context


class CompanyProfileUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = CompanyProfile
    template_name = "company/form.html"
    form_class = CompanyProfileForm
    context_object_name = "company"

    def get_object(self):
        return get_object_or_404(CompanyProfile, user__username=self.kwargs["username"])

    def get_success_url(self) -> str:
        return reverse(
            "company_profile", kwargs={"username": self.request.user.username}
        )


class ExperienceListView(LoginRequiredMixin, UserRequiredMixin, ListView):
    model = Experience
    template_name = "experience/list.html"
    context_object_name = "experiences"

    def get_queryset(self):
        return (
            Experience.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related("job_category")
        )


class ExperienceCreateView(LoginRequiredMixin, UserRequiredMixin, CreateView):
    model = Experience
    template_name = "experience/form.html"
    form_class = ExperienceForm
    success_url = reverse_lazy("experience_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ExperienceUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Experience
    template_name = "experience/form.html"
    form_class = ExperienceForm
    success_url = reverse_lazy("experience_list")


class ExperienceDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Experience
    success_url = reverse_lazy("experience_list")
    template_name = "experience/confirm_delete.html"


class EducationsListView(LoginRequiredMixin, UserRequiredMixin, ListView):
    model = Education
    template_name = "education/list.html"
    context_object_name = "educations"
    success_url = reverse_lazy("education_list")

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user).select_related("user")


class EducationsCreateView(LoginRequiredMixin, UserRequiredMixin, CreateView):
    model = Education
    template_name = "education/form.html"
    form_class = EducationForm
    success_url = reverse_lazy("education_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EducationsUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Education
    template_name = "education/form.html"
    form_class = EducationForm
    success_url = reverse_lazy("education_list")


class EducationDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Education
    template_name = "education/confirm_delete.html"
    success_url = reverse_lazy("education_list")


class UserSkillListView(LoginRequiredMixin, UserRequiredMixin, ListView):
    model = UserSkill
    template_name = "skill/list.html"
    context_object_name = "skills"

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)


class SkillsCreateView(LoginRequiredMixin, UserRequiredMixin, CreateView):
    model = UserSkill
    template_name = "skill/form.html"
    form_class = UserSkillsForm
    success_url = reverse_lazy("skill_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SkillsUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = UserSkill
    template_name = "skill/form.html"
    form_class = UserSkillsForm
    context_object_name = "skill"
    success_url = reverse_lazy("skill_list")


class SkillsDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = UserSkill
    success_url = reverse_lazy("skill_list")
