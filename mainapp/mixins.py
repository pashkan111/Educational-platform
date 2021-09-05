from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class OwnerMixin(object):
    def get_queryset(self):
        print('OwnerMixin')
        qs = super().get_queryset()
        return qs.filter(user = self.request.user)

class OwnerUpdateMixin(object):
    def form_valid(self, form):
        print('OwnerUpdateMixin')
        form.instance.user = self.request.user
        return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course

class OwnerCourseUpdateMixin(OwnerCourseMixin, OwnerUpdateMixin):
    print('OwnerCUMixin')
    fields = ['subject', 'name', 'description']
    success_url = reverse_lazy('manage')
    template_name = 'form.html'


