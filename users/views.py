# users/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import MyUserCreationForm

class RegistrationView(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'

