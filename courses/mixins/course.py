from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from ..models import Course

class CourseUpdateDeleteMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Course
    pk_url_kwarg = 'course_id'

    def test_func(self):
        author = self.get_object().author
        return self.request.user == author