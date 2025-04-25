from django.urls import path, include
# from . import views

from .views import *

app_name = 'courses'

urlpatterns = [
    path('', AllCourseListView.as_view(), name='list_all_courses'),
    path('add_course/', CourseCreateView.as_view(), name='add_course'),
    path('<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:course_id>/update/', CourseUpdateView.as_view(), name='update_course'),
    path('<int:course_id>/delete/', CourseDeleteView.as_view(), name='delete_course'),
    # path('<int:course_id>/add_lesson/', views.LessonCreateView.as_view(), name='add_lesson'),
    # path('<int:course_id>/hidden/', views.HiddenLessonListView.as_view(), name='hidden_lessons'),

    # path('lesson/<int:lesson_id>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    # path('lesson/<int:lesson_id>/update/', views.LessonUpdateView.as_view(), name='update_lesson'),
    # path('lesson/<int:lesson_id>/delete/', views.LessonDeleteView.as_view(), name='delete_lesson'),
    # path('lesson/<int:lesson_id>/add_test/', views.TestCreateView.as_view(), name='add_test'),
    # path('lesson/<int:lesson_id>/hidden/', views.HiddenTestListView.as_view(), name='hidden_tests'),
    # path('lesson/<int:lesson_id>/toggle/', views.toggle_lesson, name='toggle_lesson'),

    # path('test/<int:test_id>/', views.TestDetailView.as_view(), name='test_detail'),
    # path('test/<int:test_id>/update/', views.TestUpdateView.as_view(), name='update_test'),
    # path('test/<int:test_id>/delete/', views.TestDeleteView.as_view(), name='delete_test')
]