from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponseForbidden
class CompanyRequiredMixin(UserPassesTestMixin):
    raise_exception = False
    def test_func(self) -> bool | None:
        return self.request.user.is_company



class UserRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return  not self.request.user.is_company


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        obj = self.get_object()
        if hasattr(obj, "publisher"):
            return obj.publisher == self.request.user
        return obj.user == self.request.user