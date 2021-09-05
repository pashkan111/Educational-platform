from .views import *
from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # path('songs/', SongsViews),
    path('tasks/', TaskView.as_view({'get': 'list'})),
    path('sprints/', SprintView.as_view({'get': 'list'})),
]