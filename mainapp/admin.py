from django.contrib import admin
from .models import *

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Module)
class ModuleInline(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    # inlines = [ModuleInline]


admin.site.register(Content)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(File)
admin.site.register(Text)
