from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from ..models import Module

class ModuleUpdateDeleteMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Module
    pk_url_kwarg = 'module_id'

    def test_func(self):
        author = self.get_object().course.author
        return self.request.user == author
