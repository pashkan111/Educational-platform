from django.forms.models import modelform_factory
from django.http import HttpResponse, request
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import View
from .mixins import *
from .models import *
from .forms import *
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin
from django.apps import apps


class ManageCourse(OwnerMixin, ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'


class CreateCourse(PermissionRequiredMixin, OwnerCourseUpdateMixin, CreateView):
    permission_required = 'mainapp.add_course'
    
    
class UpdateCourse(PermissionRequiredMixin, OwnerCourseUpdateMixin, UpdateView):
    permission_required = 'mainapp.change_course'


class DeleteCourse(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    template_name = 'delete.html'
    success_url = reverse_lazy('manage')
    permission_required = 'mainapp.delete_course'

class CreateModule(TemplateResponseMixin, View):
    course = None

    def dispatch(self, request, id, *args, **kwargs):
        self.course = get_object_or_404(Course, id=id, user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwarg):
        formset = ModuleFormSet(request.POST or None)
        return render(request, 'formset.html', {'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = ModuleFormSet(instance=self.course, data=request.POST or None)
        if formset.is_valid():
            formset.save()
            return redirect('manage')
        return self.get(request)


class ContentCreateUpdateView(TemplateResponseMixin, View):
    model=None
    module=None
    object=None
    template_name='module_form.html'

    def get_model(self, model):
        if model in ['text', 'file', 'image', 'video']:
            return apps.get_model(app_label='mainapp', model_name=model)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['created', 'updated', 'owner'])
        return Form( *args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None, *args, **kwargs):
        self.module = get_object_or_404(Module, id=module_id, course__user=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.object = get_object_or_404(self.model, id=id, user=request.user)        
        return super().dispatch(request, module_id, model_name, id=None, *args, **kwargs)

    def get(self,request, *args, **kwargs):
        form = self.get_form(self.model, instance=self.object)
        return render(request, 'module_form.html', {'form': form, 'object': self.object})

    def post(self,request, *args, **kwargs):
        form = self.get_form(self.get_model,
            data=request.POST,
            files=request.FILES,
            instanse=self.object
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not request.POST.get('id'):
                Content.objects.create(module=self.module, item=obj)
                return redirect('manage')
            return self.get(request)


class ContentDelete(View):
    def post(self, request):
        content_id = request.POST.get('id')
        content = Content.objects.get_object_or_404(id=content_id)
        content.item.delete()
        return redirect('manage')


class CourseModulesView(View):
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        modules = course.module_course.all()
        return render(request, 'course_detail.html', {'modules': modules})


class ModuleContentView(View):
    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        content = module.contents.all()
        return render(request, 'module_detail.html', {'content': content})
