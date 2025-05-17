from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Lesson, Module, Test
from ..forms import LessonForm
from ..mixins import LessonUpdateDeleteMixin, BaseDeleteMixin


class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'courses/create_update_form.html'

    def test_func(self):
        author = Module.objects.get(pk=self.kwargs.get('module_id')).course.author
        return self.request.user == author

    def form_valid(self, form):
        module = Module.objects.get(pk=self.kwargs.get('module_id'))
        lesson_number = Lesson.objects.filter(module=module).count() + 1
        form.instance.module = module
        form.instance.lesson_number = lesson_number
        self.object = form.save()
        kwargs = {'lesson_id': self.object.pk}
        redirect = reverse_lazy('courses:lesson_detail', kwargs=kwargs)
        return HttpResponseRedirect(redirect)
    

class LessonDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Lesson
    template_name = 'courses/lesson/lesson_detail.html'
    pk_url_kwarg = 'lesson_id'

    def test_func(self):
        lesson = self.get_object()
        if lesson.hidden:
            return self.request.user == lesson.module.course.author
        return True

    ### TODO ###
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = Test.objects.filter(lesson=self.kwargs.get('lesson_id'), hidden=False)
        return context
    

class LessonUpdateView(LessonUpdateDeleteMixin, UpdateView):
    form_class = LessonForm
    template_name = 'courses/create_update_form.html'

    def get_success_url(self):
        kwargs = {'lesson_id': self.kwargs.get('lesson_id')}
        return reverse_lazy('courses:lesson_detail', kwargs=kwargs)


class LessonDeleteView(LessonUpdateDeleteMixin, BaseDeleteMixin):

    def post(self, request, *args, **kwargs):
        lesson_number = self.get_object().lesson_number
        updating_lessons = Lesson.objects.filter(lesson_number__gt=lesson_number)
        for lesson in updating_lessons:
            lesson.lesson_number -= 1
            lesson.save()
        return super().post(request, *args, **kwargs)

    def get_delete_name(self):
        return self.get_object().name
    
    def get_success_url(self):
        kwargs = {'module_id': self.get_object().module.pk}
        return reverse_lazy('courses:module_detail', kwargs=kwargs)


class HiddenLessonListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Lesson
    template_name = 'courses/lesson/hidden_lesson_list.html'

    def test_func(self):
        author = Module.objects.get(pk=self.kwargs.get('module_id')).course.author
        return self.request.user == author

    def get_queryset(self):
        return Lesson.objects.filter(module=self.kwargs.get('module_id'), hidden=True)


@login_required
def toggle_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if lesson.module.course.author == request.user:
        lesson.hidden = not lesson.hidden
        lesson.save()

    return redirect('courses:lesson_detail', lesson_id=lesson_id)