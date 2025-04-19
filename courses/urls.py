from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Student views
    path('', views.CourseListView.as_view(), name='course_list'),
    path('create/', views.create_course, name='create_course'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    
    # Teacher views
    path('teacher/', views.TeacherCourseListView.as_view(), name='teacher_course_list'),
    path('teacher/course/<int:pk>/', views.TeacherCourseDetailView.as_view(), name='teacher_course_detail'),

    path('<int:course_id>/create-lesson/', views.create_lesson, name='create_lesson'),
    path('<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('<int:course_id>/lesson/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('<int:course_id>/lesson/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
] 