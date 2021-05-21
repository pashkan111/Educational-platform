from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
User = get_user_model()

class Subject(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
    related_name='%(class)s_related',
    on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()

class Content(models.Model):
    module = models.ForeignKey(Module,
    related_name='contents',
    on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in':(
        'text',
        'video',
        'image',
        'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')



