from django.urls import path, include
from . import views

app_name = 'courses'

urlpatterns = [
    path('list_courses/', views.CoursesList.as_view(), name='list_courses'),
    path('add_course/', views.CourseCreateView.as_view(), name='add_course')
]