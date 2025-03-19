from django.urls import path

from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('auth', views.auth_page, name='auth_page')
]