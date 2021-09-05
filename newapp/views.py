from rest_framework import viewsets
from .serializers import *
from .models import *
from .utils import DefaultMixin


class SprintView(DefaultMixin, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer

class TaskView(DefaultMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer



