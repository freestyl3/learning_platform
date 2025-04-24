from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from . import models, forms


# COURSE


class CoursesList(ListView):
    model = models.Course
    template_name = 'courses/course/list_courses.html'


class CourseCreateView(LoginRequiredMixin, CreateView):
    form_class = forms.CourseForm
    model = models.Course
    template_name = 'courses/create_update_form.html'
    success_url = reverse_lazy('courses:list_courses')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class CourseUpdateDeleteMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = models.Course

    def test_func(self):
        author = get_object_or_404(models.Course, pk=self.kwargs.get('course_id')).author
        return self.request.user == author
    
    def get_object(self):
        return get_object_or_404(models.Course, pk=self.kwargs.get('course_id'))
    

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = models.Course
    template_name = 'courses/course/course_detail.html'
    
    def get_object(self):
        return get_object_or_404(models.Course, pk=self.kwargs.get('course_id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = models.Lesson.objects.filter(course_id=self.kwargs.get('course_id'), hidden=False)
        return context
    

class CourseUpdateView(CourseUpdateDeleteMixin, UpdateView):
    form_class = forms.CourseForm
    template_name = 'courses/create_update_form.html'
    
    def get_success_url(self):
        kwargs = {'course_id': self.kwargs.get('course_id')}
        return reverse_lazy('courses:course_detail', kwargs=kwargs)
    

class CourseDeleteView(CourseUpdateDeleteMixin, DeleteView):
    template_name = 'courses/course/delete_course.html'
    success_url = reverse_lazy('courses:list_courses')


# LESSON


class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.Lesson
    form_class = forms.LessonForm
    template_name = 'courses/create_update_form.html'

    def test_func(self):
        author = get_object_or_404(models.Course, pk=self.kwargs.get('course_id')).author
        return self.request.user == author

    def get_success_url(self):
        kwargs = {'course_id': self.kwargs.get('course_id')}
        return reverse_lazy('courses:course_detail', kwargs=kwargs)

    def form_valid(self, form):
        course = get_object_or_404(models.Course, pk=self.kwargs.get('course_id'))
        form.instance.course_id = course
        return super().form_valid(form)
    

class LessonDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = models.Lesson
    template_name = 'courses/lesson/lesson_detail.html'

    def test_func(self):
        lesson = get_object_or_404(models.Lesson, pk=self.kwargs.get('lesson_id'))
        if lesson.hidden:
            return self.request.user == lesson.course_id.author
        return True

    def get_object(self):
        return get_object_or_404(models.Lesson, pk=self.kwargs.get('lesson_id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = models.Test.objects.filter(lesson_id=self.kwargs.get('lesson_id'), hidden=False)
        return context
    

class LessonUpdateDeleteMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = models.Lesson

    def test_func(self):
        author = get_object_or_404(models.Lesson, pk=self.kwargs.get('lesson_id')).course_id.author
        return self.request.user == author
    
    def get_object(self):
        return get_object_or_404(models.Lesson, pk=self.kwargs.get('lesson_id'))
    
    # UPDATE
    

class LessonUpdateView(LessonUpdateDeleteMixin, UpdateView):
    form_class = forms.LessonForm
    template_name = 'courses/create_update_form.html'   

    def get_success_url(self):
        kwargs = {'lesson_id': self.kwargs.get('lesson_id')}
        return reverse_lazy('courses:lesson_detail', kwargs=kwargs)

class LessonDeleteView(LessonUpdateDeleteMixin, DeleteView):
    template_name = 'courses/lesson/delete_lesson.html'
    success_url = reverse_lazy('courses:list_courses')

    # UPDATE


class HiddenLessonListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Lesson
    template_name = 'courses/lesson/hidden_lesson_list.html'

    def test_func(self):
        author = get_object_or_404(models.Course, pk=self.kwargs.get('course_id')).author
        return self.request.user == author

    def get_queryset(self):
        return models.Lesson.objects.filter(course_id=self.kwargs.get('course_id'), hidden=True)


@login_required
def toggle_lesson(request, lesson_id):
    lesson = get_object_or_404(models.Lesson, pk=lesson_id)
    if lesson.course_id.author == request.user:
        lesson.hidden = not lesson.hidden
        lesson.save()

    return redirect('courses:lesson_detail', lesson_id=lesson_id)


# TEST


class TestCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.Test
    form_class = forms.TestForm
    template_name = 'courses/create_update_form.html'

    def test_func(self):
        author = get_object_or_404(models.Lesson, pk=self.kwargs.get('lesson_id')).course_id.author
        return self.request.user == author
    
    def form_valid(self, form):
        form.instance.lesson_id = models.Lesson.objects.get(pk=self.kwargs.get('lesson_id'))
        return super().form_valid(form)
    
    def get_success_url(self):
        kwargs = {'lesson_id': self.kwargs.get('lesson_id')}
        return reverse_lazy('courses:lesson_detail', kwargs=kwargs)
    

class HiddenTestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Test
    template_name = 'courses/test/hidden_test_list.html'

    def test_func(self):
        author = get_object_or_404(models.Lesson, pk=self.kwargs.get('lesson_id')).course_id.author
        return self.request.user == author

    def get_queryset(self):
        return models.Test.objects.filter(lesson_id=self.kwargs.get('lesson_id'), hidden=True)
    

class TestDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = models.Test
    template_name = 'courses/test/test_detail.html'
    
    def get_object(self):
        return get_object_or_404(models.Test, pk=self.kwargs.get('test_id'))
    
    def test_func(self):
        test = self.get_object()
        if test.hidden:
            return self.request.user == test.lesson_id.course_id.author
        return True
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['questions'] = models.Question.objects.filter(lesson_id=self.kwargs.get('lesson_id'))
    #     return context


class TestUpdateDeleteMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = models.Test

    def test_func(self):
        author = get_object_or_404(models.Test, pk=self.kwargs.get('test_id')).lesson_id.course_id.author
        return self.request.user == author
    
    def get_object(self):
        return get_object_or_404(models.Test, pk=self.kwargs.get('test_id'))
    

class TestUpdateView(TestUpdateDeleteMixin, UpdateView):
    form_class = forms.TestForm
    template_name = 'courses/create_update_form.html'

    def get_success_url(self):
        kwargs = {'test_id': self.kwargs.get('test_id')}
        return reverse_lazy('courses:test_detail', kwargs=kwargs)
    

class TestDeleteView(TestUpdateDeleteMixin, DeleteView):
    template_name = 'courses/test/delete_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(models.Test, pk=self.kwargs.get('test_id'))
        form = forms.TestForm(instance=instance)
        context['form'] = form
        context['model'] = models.Test._meta.verbose_name
        return context

    def get_success_url(self):
        lesson = get_object_or_404(models.Test, pk=self.kwargs.get('test_id')).lesson_id
        kwargs = {'lesson_id': lesson.pk}
        return reverse_lazy('courses:lesson_detail', kwargs=kwargs)
    
