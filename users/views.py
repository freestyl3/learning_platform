from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import MyUserCreationForm
import logging

logger = logging.getLogger(__name__)

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)

class SignUpView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('homepage:homepage')

    def form_valid(self, form):
        logger.info("Starting registration process")
        try:
            # Save the user first
            user = form.save()
            logger.info(f"User {user.username} created successfully")
            
            # Then authenticate and login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            logger.info(f"Attempting to authenticate user {username}")
            
            user = authenticate(username=username, password=password)
            if user is not None:
                logger.info(f"User {username} authenticated successfully")
                login(self.request, user)
                logger.info(f"User {username} logged in successfully")
            else:
                logger.error(f"Failed to authenticate user {username}")
            
            return redirect(self.success_url)
        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            raise
