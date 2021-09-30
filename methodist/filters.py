from django_filters.rest_framework import FilterSet
from django.forms import TextInput, DateField

from .models import Student


class StudentFilter(FilterSet):
    year_entry = DateField(widget=TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Student
        fields = ('year_entry', 'group', 'educational_program', 'user__username', 'user__last_name')


def filter_student(request, qs):
    if request.GET.get('year_entry'):
        qs = qs.filter(year_entry=request.GET.get('year_entry'))

    if request.GET.get('group'):
        qs = qs.filter(group_id=request.GET.get('group'))

    if request.GET.get('educational_program'):
        qs = qs.filter(educational_program_id=request.GET.get('educational_program'))

    if request.GET.get('user__username'):
        qs = qs.filter(user__username=request.GET.get('user__username'))

    if request.GET.get('user__last_name'):
        qs = qs.filter(user__last_name=request.GET.get('user__last_name'))

    return qs