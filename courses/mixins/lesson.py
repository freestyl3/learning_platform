from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from ..models import Lesson

class LessonUpdateDeleteMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Lesson
    pk_url_kwarg = 'lesson_id'

    def test_func(self):
        author = self.get_object().module.course.author
        return self.request.user == author
