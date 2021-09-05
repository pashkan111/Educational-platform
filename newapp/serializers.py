from django.db.models import fields
from rest_framework import serializers
from .models import Sprint, Task, User
from rest_framework.reverse import reverse 

class SprintSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField('get_links')
    class Meta:
        model=Sprint
        fields=('id', 'name', 'description', 'end', 'links')

    def get_links(self, obj): 
        request = self.context['request']
        return {
        'self': reverse('sprint-detail',
        kwargs={'pk': obj.pk},request=request),
        }

class TaskSerializer(serializers.ModelSerializer):
    assigned = serializers.SlugRelatedField(
        slug_field=User.USERNAME_FIELD, required=False, read_only=True
    )
    sprint = serializers.SlugRelatedField(slug_field='name', read_only=True)
    status_d = serializers.SerializerMethodField('get_status', read_only=True)
    class Meta:
        model=Task
        fields=(
            'id', 'name', 'description', 'sprint', 'order', 'assigned', 'started', 'due', 'completed', 'status_d'
        )

    def get_status(self, object):
        return object.get_stat_display()