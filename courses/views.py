from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
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

# Create your views here.
