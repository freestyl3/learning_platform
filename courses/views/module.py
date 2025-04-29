from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from ..forms import ModuleForm
from ..mixins import BaseDeleteMixin, ModuleUpdateDeleteMixin
from ..models import Course, Module, Lesson


class ModuleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'courses/create_update_form.html'
    pk_url_kwarg = 'course_id'

    def test_func(self):
        author = Course.objects.get(pk=self.kwargs.get(self.pk_url_kwarg)).author
        return self.request.user == author

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs.get('course_id'))
        module_number = Module.objects.filter(course=course).count() + 1
        form.instance.course = course
        form.instance.module_number = module_number
        self.object = form.save()
        kwargs = {'module_id': self.object.pk}
        redirect = reverse_lazy('courses:module_detail', kwargs=kwargs)
        return HttpResponseRedirect(redirect)
    

class ModuleDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Module
    template_name = 'courses/module/module_detail.html'
    pk_url_kwarg = 'module_id'

    def test_func(self):
        module = self.get_object()
        if module.hidden:
            return self.request.user == module.course.author
        return True
    
    ### TODO ###
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(module=self.get_object(), hidden=False)
        # context['tests'] = models.Test.objects.filter(lesson_id=self.kwargs.get('lesson_id'), hidden=False)
        return context
    

class ModuleUpdateView(ModuleUpdateDeleteMixin, UpdateView):
    form_class = ModuleForm
    template_name = 'courses/create_update_form.html'

    def get_success_url(self):
        kwargs = {'module_id': self.kwargs.get(self.pk_url_kwarg)}
        return reverse_lazy('courses:module_detail', kwargs=kwargs)


class ModuleDeleteView(ModuleUpdateDeleteMixin, BaseDeleteMixin):
    # form_class = ModuleForm

    def get_delete_name(self):
        return self.get_object().name
    
    def get_success_url(self):
        kwargs = {'course_id': self.get_object().course.pk}
        return reverse_lazy('courses:course_detail', kwargs=kwargs)


class HiddenModuleListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Module
    template_name = 'courses/module/hidden_module_list.html'

    def test_func(self):
        author = Course.objects.get(pk=self.kwargs.get('course_id')).author
        return self.request.user == author

    def get_queryset(self):
        return Module.objects.filter(course=self.kwargs.get('course_id'), hidden=True)


@login_required
def toggle_module(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    if module.course.author == request.user:
        module.hidden = not module.hidden
        module.save()

    return redirect('courses:module_detail', module_id=module_id)
