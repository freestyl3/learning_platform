from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . import models, forms


# COURSE


class CoursesList(ListView):
    model = models.Course
    template_name = 'courses/list_courses.html'


class CourseCreateView(LoginRequiredMixin, CreateView):
    form_class = forms.CourseForm
    model = models.Course
    template_name = 'courses/add_course.html'
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
    template_name = 'courses/course_detail.html'
    
    def get_object(self):
        return get_object_or_404(models.Course, pk=self.kwargs.get('course_id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = models.Lesson.objects.filter(course_id=self.kwargs.get('course_id'), hidden=False)
        return context
    

class CourseUpdateView(CourseUpdateDeleteMixin, UpdateView):
    form_class = forms.CourseForm
    template_name = 'courses/add_course.html'
    
    def get_success_url(self):
        kwargs = {'course_id': self.kwargs.get('course_id')}
        return reverse_lazy('courses:course_detail', kwargs=kwargs)
    

class CourseDeleteView(CourseUpdateDeleteMixin, DeleteView):
    template_name = 'courses/delete_course.html'
    success_url = reverse_lazy('courses:list_courses')


# LESSON


class LessonCreateView(LoginRequiredMixin, CreateView):
    model = models.Lesson
    form_class = forms.LessonForm
    template_name = 'courses/add_lesson.html'

    def get_success_url(self):
        kwargs = {'course_id': self.kwargs.get('course_id')}
        return reverse_lazy('courses:course_detail', kwargs=kwargs)

    def form_valid(self, form):
        course = get_object_or_404(models.Course, pk=self.kwargs.get('course_id'))
        form.instance.course_id = course
        return super().form_valid(form)
    

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = models.Lesson
    template_name = 'courses/lesson_detail.html'

    def get_object(self):
        return get_object_or_404(models.Lesson, pk=self.kwargs.get('lesson_id'))
    

class LessonUpdateDeleteMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = models.Lesson

    def test_func(self):
        author = get_object_or_404(models.Lesson, pk=self.kwargs.get('lesson_id')).course_id.author
        return self.request.user == author
    
    def get_object(self):
        return get_object_or_404(models.Lesson, pk=self.kwargs.get('lesson_id'))
    

class LessonUpdateView(LessonUpdateDeleteMixin, UpdateView):
    form_class = forms.LessonForm
    template_name = 'courses/add_lesson.html'    

    def get_success_url(self):
        kwargs = {'lesson_id': self.kwargs.get('lesson_id')}
        return reverse_lazy('courses:lesson_detail', kwargs=kwargs)

class LessonDeleteView(LessonUpdateDeleteMixin, DeleteView):
    template_name = 'courses/delete_lesson.html'
    success_url = reverse_lazy('courses:list_courses')
