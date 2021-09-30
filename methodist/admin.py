from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class StudentTabAdmin(admin.TabularInline):
    model = Student


@admin.register(CustomUser)
class CustomerAdmin(UserAdmin):
    """ For custom model `User`
    """
    change_form_template = 'methodist/admin.html'

    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'department', 'group')
    search_fields = ('first_name', 'last_name')
    list_filter = ('group', 'department')
    inlines = [StudentTabAdmin]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'surname')}),
        (_('Additional Info'), {'fields': ('department', 'group')}),
         # (_('Permissions'), {
         #   'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
         # }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(EducationalProgram)
class EducationalProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_subject', 'group', 'form_of_control')
    readonly_fields = ('loans',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'year_entry', 'educational_program')


@admin.register(Rating)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'rating_5')


@admin.register(Permissions)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
