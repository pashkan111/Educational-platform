from django.urls import path, include
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('mine/', ManageCourse.as_view(), name = 'manage'),
    path('create/', CreateCourse.as_view(), name = 'create'),
    path('edit/<int:pk>', UpdateCourse.as_view(), name = 'update'),
    path('delete/<int:pk>', DeleteCourse.as_view(), name = 'delete'),
    path('home/', views.LoginView.as_view(),name = 'home'),
    path('module/<int:id>/', CreateModule.as_view(),name = 'create-module'),
    path('module/<int:module_id>/content/<str:model_name>/create/', ContentCreateUpdateView.as_view(),name = 'create-content'),
    path('module/<int:module_id>/content/<str:model_name>/id/', ContentCreateUpdateView.as_view(),name = 'update-content'),
    path('course/<int:id>/delete/', ContentDelete.as_view(), name = 'delete-content'),
    path('course-detail/<int:course_id>/', CourseModulesView.as_view(), name = 'course-detail'),
    path('module-detail/<int:module_id>/', ModuleContentView.as_view(), name = 'module-detail'),
]
