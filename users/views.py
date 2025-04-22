# users/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView

from .forms import MyUserCreationForm

class CustomLoginView(LoginView):
    success_url = reverse_lazy('courses')
    template_name = 'registration/login.html'

class RegistrationView(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'

