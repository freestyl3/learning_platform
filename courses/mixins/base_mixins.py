from django.views.generic import DeleteView

class BaseDeleteMixin(DeleteView):
    template_name = 'courses/delete_form.html'

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    def get_delete_name(self):
        return self.get_object().pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # instance = self.get_object()
        # form = self.form_class(instance=instance)
        # context['form'] = form
        context['delete_name'] = self.get_delete_name()
        context['model'] = self.model._meta.verbose_name
        return context