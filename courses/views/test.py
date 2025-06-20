from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from ..models import Test, Lesson
from ..forms import TestForm
from ..mixins import BaseDeleteMixin, TestUpdateDeleteMixin

class TestCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Test
    form_class = TestForm
    template_name = 'courses/create_update_form.html'

    def test_func(self):
        author = get_object_or_404(Lesson, pk=self.kwargs.get('lesson_id')).module.course.author
        return self.request.user == author
    
    def form_valid(self, form):
        lesson = Lesson.objects.get(pk=self.kwargs.get('lesson_id'))
        test_number = Test.objects.filter(lesson=lesson).count() + 1
        form.instance.lesson = lesson
        form.instance.test_number = test_number
        self.object = form.save()
        kwargs = {'test_id': self.object.pk}
        redirect = reverse_lazy('courses:test_detail', kwargs=kwargs)
        return HttpResponseRedirect(redirect)
    
    # def form_valid(self, form):
    #     form.instance.lesson = Lesson.objects.get(pk=self.kwargs.get('lesson_id'))
    #     return super().form_valid(form)
    
    # def get_success_url(self):
    #     kwargs = {'lesson_id': self.kwargs.get('lesson_id')}
    #     return reverse_lazy('courses:lesson_detail', kwargs=kwargs)
    

class HiddenTestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Test
    template_name = 'courses/test/hidden_test_list.html'

    def test_func(self):
        author = get_object_or_404(Lesson, pk=self.kwargs.get('lesson_id')).module.course.author
        return self.request.user == author

    def get_queryset(self):
        return Test.objects.filter(lesson=self.kwargs.get('lesson_id'), hidden=True)
    

class TestDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Test
    template_name = 'courses/test/test_detail.html'
    pk_url_kwarg = 'test_id'
    
    def test_func(self):
        test = self.get_object()
        if test.hidden:
            return self.request.user == test.lesson.module.course.author
        return True
    

    ### TODO ###
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['questions'] = models.Question.objects.filter(lesson_id=self.kwargs.get('lesson_id'))
    #     return context
    

class TestUpdateView(TestUpdateDeleteMixin, UpdateView):
    form_class = TestForm
    template_name = 'courses/create_update_form.html'

    def get_success_url(self):
        kwargs = {'test_id': self.kwargs.get('test_id')}
        return reverse_lazy('courses:test_detail', kwargs=kwargs)
    

class TestDeleteView(TestUpdateDeleteMixin, BaseDeleteMixin):
    # form_class = TestForm

    def get_delete_name(self):
        return self.get_object().name
    
    def get_success_url(self):
        kwargs = {'lesson_id': self.get_object().lesson.pk}
        return reverse_lazy('courses:lesson_detail', kwargs=kwargs)