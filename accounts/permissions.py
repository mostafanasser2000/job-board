from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect


class CompanyRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and self.request.user.is_company

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("jobs_list")


class UserRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and not self.request.user.is_company

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("jobs_list")


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.user == self.request.user

    def handle_no_permission(self):
        return redirect("job_list")
