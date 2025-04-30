from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from ..models import Test

class TestUpdateDeleteMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Test
    pk_url_kwarg = 'test_id'

    def test_func(self):
        author = self.get_object().lesson.module.course.author
        return self.request.user == author
