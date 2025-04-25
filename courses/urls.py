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

    path('module/<int:module_id>/', ModuleDetailView.as_view(), name='module_detail'),
    path('module/<int:module_id>/update/', ModuleUpdateView.as_view(), name='update_module'),
    path('module/<int:module_id>/delete/', ModuleDeleteView.as_view(), name='delete_module'),
    # path('lesson/<int:lesson_id>/add_test/', views.TestCreateView.as_view(), name='add_test'),
    # path('lesson/<int:lesson_id>/hidden/', views.HiddenTestListView.as_view(), name='hidden_tests'),
    path('module/<int:module_id>/toggle/', toggle_module, name='toggle_module'),

    # path('test/<int:test_id>/', views.TestDetailView.as_view(), name='test_detail'),
    # path('test/<int:test_id>/update/', views.TestUpdateView.as_view(), name='update_test'),
    # path('test/<int:test_id>/delete/', views.TestDeleteView.as_view(), name='delete_test')
]