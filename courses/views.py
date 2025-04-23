from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from . import models, forms

class CoursesList(LoginRequiredMixin, ListView):
    model = models.Course
    template_name = 'courses/list_courses.html'


class CourseCreateView(LoginRequiredMixin, CreateView):
    form_class = forms.CreateCourseForm
    model = models.Course
    template_name = 'courses/add_course.html'
    success_url = reverse_lazy('courses:list_courses')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = models.Course
    template_name = 'courses/course_detail.html'
    
    def get_object(self):
        return get_object_or_404(models.Course, pk=self.kwargs.get('course_id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = models.Lesson.objects.filter(course_id=self.kwargs.get('course_id'), hidden=False)
        return context

# Create your views here.
