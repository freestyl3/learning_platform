from django.urls import path, include
from . import views

app_name = 'courses'

urlpatterns = [
    path('list_courses/', views.CoursesList.as_view(), name='list_courses'),
    path('add_course/', views.CourseCreateView.as_view(), name='add_course'),
    path('<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<int:course_id>/update/', views.CourseUpdateView.as_view(), name='update_course'),
    path('<int:course_id>/delete/', views.CourseDeleteView.as_view(), name='delete_course'),
    path('<int:course_id>/add_lesson/', views.LessonCreateView.as_view(), name='add_lesson'),

    path('lesson/<int:lesson_id>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/<int:lesson_id>/update/', views.LessonUpdateView.as_view(), name='update_lesson'),
    path('lesson/<int:lesson_id>/delete/', views.LessonDeleteView.as_view(), name='delete_lesson')
]