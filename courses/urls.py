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
    path('<int:course_id>/add_module/', ModuleCreateView.as_view(), name='add_module'),
    path('<int:course_id>/hidden/', HiddenModuleListView.as_view(), name='hidden_modules'),
    path('<int:course_id>/toggle_subscribe/', toggle_subscribe, name='toggle_subscribe'),
    path('my_subscribes/', MySubscribeListView.as_view(), name='my_subscribes'),
    path('created_courses/', CreatedCourseListView.as_view(), name='created_courses'),

    path('module/<int:module_id>/', ModuleDetailView.as_view(), name='module_detail'),
    path('module/<int:module_id>/update/', ModuleUpdateView.as_view(), name='update_module'),
    path('module/<int:module_id>/delete/', ModuleDeleteView.as_view(), name='delete_module'),
    path('module/<int:module_id>/toggle_module/', toggle_module, name='toggle_module'),
    path('module/<int:module_id>/add_lesson/', LessonCreateView.as_view(), name='add_lesson'),
    path('module/<int:module_id>/hidden', HiddenLessonListView.as_view(), name='hidden_lessons'),

    path('lesson/<int:lesson_id>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/<int:lesson_id>/update/', LessonUpdateView.as_view(), name='update_lesson'),
    path('lesson/<int:lesson_id>/delete/', LessonDeleteView.as_view(), name='delete_lesson'),
    path('lesson/<int:lesson_id>/toggle_lesson/', toggle_lesson, name='toggle_lesson'),
    # path('lesson/<int:lesson_id>/add_test/', views.TestCreateView.as_view(), name='add_test'),
    # path('lesson/<int:lesson_id>/hidden/', views.HiddenTestListView.as_view(), name='hidden_tests'),
    # path('test/<int:test_id>/', views.TestDetailView.as_view(), name='test_detail'),
    # path('test/<int:test_id>/update/', views.TestUpdateView.as_view(), name='update_test'),
    # path('test/<int:test_id>/delete/', views.TestDeleteView.as_view(), name='delete_test')
]