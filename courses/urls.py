from django.urls import path, include
from . import views

app_name = 'courses'

urlpatterns = [
    path('list_courses/', views.CoursesList.as_view(), name='list_courses'),
    path('add_course/', views.CourseCreateView.as_view(), name='add_course'),
    path('<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<int:course_id>/update/', views.CourseUpdateView.as_view(), name='update_course'),
    path('<int:course_id>/delete/', views.CourseDeleteView.as_view(), name='delete_course')
]