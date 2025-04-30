from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from ..forms import CourseForm
from ..mixins import BaseDeleteMixin, CourseUpdateDeleteMixin
from ..models import Course, Module, UsersCourses


class AllCourseListView(ListView):
    model = Course
    template_name = 'courses/course/list_courses.html'


class CourseCreateView(LoginRequiredMixin, CreateView):
    form_class = CourseForm
    model = Course
    template_name = 'courses/create_update_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        kwargs = {'course_id': self.object.pk}
        redirect = reverse_lazy('courses:course_detail', kwargs=kwargs)
        return HttpResponseRedirect(redirect)


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course/course_detail.html'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = Module.objects.filter(
            course=self.get_object(), hidden=False
        )
        context['is_subscribed'] = UsersCourses.objects.filter(
            user=self.request.user,
            course=self.get_object()
        ).exists()
        return context


class CourseUpdateView(CourseUpdateDeleteMixin, UpdateView):
    form_class = CourseForm
    template_name = 'courses/create_update_form.html'

    def get_success_url(self):
        kwargs = {'course_id': self.kwargs.get('course_id')}
        return reverse_lazy('courses:course_detail', kwargs=kwargs)


class CourseDeleteView(CourseUpdateDeleteMixin, BaseDeleteMixin):
    # form_class = CourseForm
    success_url = reverse_lazy('courses:list_all_courses')

    def get_delete_name(self):
        return self.get_object().name
    

class MySubscribeListView(LoginRequiredMixin, AllCourseListView):
    def get_queryset(self):
        courses = Course.objects.filter(
            users=self.request.user
        )
        return courses
    

class CreatedCourseListView(LoginRequiredMixin, AllCourseListView):
    def get_queryset(self):
        courses = Course.objects.filter(
            author=self.request.user
        )
        return courses

@login_required
def toggle_subscribe(request, course_id):
    course = Course.objects.get(pk=course_id)
    subcribe = UsersCourses.objects.filter(
        course=course,
        user=request.user
    )
    if request.user != course.author:
        if not(subcribe.exists()):
            UsersCourses.objects.create(
                user=request.user,
                course=course
            )
        else:
            subcribe.delete()
        return redirect('courses:course_detail', course_id=course_id)
    return HttpResponseForbidden()
