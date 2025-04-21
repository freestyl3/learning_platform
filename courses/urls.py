from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Student views
    path('', views.CourseListView.as_view(), name='course_list'),
    path('create/', views.create_course, name='create_course'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    
    # Teacher views
    path('teacher/', views.TeacherCourseListView.as_view(), name='teacher_course_list'),
    path('teacher/course/<int:pk>/', views.TeacherCourseDetailView.as_view(), name='teacher_course_detail'),

    path('<int:course_id>/create-lesson/', views.create_lesson, name='create_lesson'),
    path('<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('<int:course_id>/lesson/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('<int:course_id>/lesson/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    
    # Test views
    path('<int:course_id>/lesson/<int:lesson_id>/create-test/', views.create_test, name='create_test'),
    path('<int:course_id>/lesson/<int:lesson_id>/test/<int:test_id>/edit/', views.edit_test, name='edit_test'),
    path('<int:course_id>/lesson/<int:lesson_id>/test/<int:test_id>/delete/', views.delete_test, name='delete_test'),
    path('<int:course_id>/lesson/<int:lesson_id>/test/<int:test_id>/add-question/', views.add_question, name='add_question'),
    path('<int:course_id>/lesson/<int:lesson_id>/test/<int:test_id>/question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/tests/<int:test_id>/take/', views.take_test, name='take_test'),

    path('tests/<int:test_id>/', views.TestListView.as_view(), name='test_results')
] 