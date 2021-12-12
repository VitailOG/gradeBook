from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import View
from django.contrib.auth.views import LoginView, LogoutView

from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login

from .models import *
from .forms import SubjectsForm, StudentForm, RatingForm, AuthForm
from .filters import StudentFilter, filter_student
from .mixins import StudentMixin, AbstractRatingMixin
from .permissions import LoginRequiredAndMethodistPermissions


class LoginRequiredAndMethodistMixin(LoginRequiredAndMethodistPermissions):
    user = "Методист"


class ListSubjectsView(LoginRequiredAndMethodistMixin, ListView):
    """ List subject on department
    """

    model = Subject
    queryset = Subject.objects.prefetch_related('teachers').select_related('group').all()
    template_name = 'methodist/subject.html'
    context_object_name = 'subjects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # form for create new subject
        context['form'] = SubjectsForm(user=self.request.user)
        return context
    

class CreateSubjectsView(LoginRequiredAndMethodistMixin, CreateView):
    model = Subject
    form_class = SubjectsForm
    success_url = reverse_lazy('list-subjects')

    def form_valid(self, form):
        super().form_valid(form)
        
        return JsonResponse({'created_subject': True, "subject_id": form.instance.id})
    
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['request'] = self.request.user
    #     return kwargs

class SemestersView(LoginRequiredAndMethodistMixin, DetailView):
    template_name = 'methodist/semesters.html'
    model = Subject
    context_object_name = 'semesters'


class DeleteSubjectsView(LoginRequiredAndMethodistMixin, DeleteView):
    model = Subject
    form_class = SubjectsForm
    success_url = reverse_lazy('list-subjects')

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'delete': True})


class UpdateSubjectsView(LoginRequiredAndMethodistMixin, UpdateView):
    model = Subject
    form_class = SubjectsForm
    success_url = reverse_lazy('list-subjects')

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'update_subject': True})


class CreateStudentView(LoginRequiredAndMethodistMixin, CreateView):
    form_class = StudentForm
    success_url = reverse_lazy('without')
    
    def form_valid(self, form):
        form.instance.user_id = self.kwargs.get('pk')
        super().form_valid(form)
        return JsonResponse({'created_student': True})

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({
    #         'files': self.request.user,
    #     })
    #     return kwargs

    
class StudentWithOutGroupView(LoginRequiredAndMethodistMixin, StudentMixin, ListView):
    model = CustomUser
    template_name = 'methodist/without_group.html'
    context_object_name = 'students'
    
    def get_queryset(self):
        return CustomUser.objects.exclude(student__year_entry__isnull=False).filter(group_id=1, department=self.request.user.department)


class StudentsView(StudentMixin, ListView):
    model = Student
    template_name = 'methodist/students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = StudentFilter(self.request.GET,
                           queryset=Student.objects.filter(user__department=self.request.user.department))

        context['students'] = qs.queryset.select_related('group', 'educational_program', 'user')
        context['student_filter'] = qs.form
        return context


class UpdateStudentView(LoginRequiredAndMethodistMixin, UpdateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('list_student')

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'update': True})


class DeleteStudentView(LoginRequiredAndMethodistMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('list_student')

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'delete': True})


o = {
    'ordering': ''
}


class FilterStudentView(LoginRequiredAndMethodistMixin, View):
    def get(self, request, *args, **kwargs):
        ord = self.request.GET.get('ordering')
        if o['ordering'] and o['ordering'] == ord:
            ord = '-' + ord
        o['ordering'] = ord
        qs = Student.objects.filter(user__department=self.request.user.department).values('id',
                                    'user__first_name',
                                    'user__last_name',
                                    'user__surname',
                                    'year_entry',
                                    'educational_program__name',
                                    'group__name',
                                    'form_education').order_by(ord if ord else 'id')

        qs = filter_student(self.request, qs)
        print('1')
        return JsonResponse({'students': list(qs)})


class RatingView(AbstractRatingMixin):
    template_name = 'methodist/rating.html'


class RatingYearView(AbstractRatingMixin):
    template_name = 'methodist/rating_year.html'


class CreateRatingView(LoginRequiredAndMethodistMixin, CreateView):
    model = Rating
    form_class = RatingForm

    def form_valid(self, form):
        form.instance.user_id = self.kwargs.get('pk_user')
        form.instance.subject_id = self.kwargs.get('pk_subject')
        super().form_valid(form)
        return JsonResponse({'create': True, 'rating_id': form.instance.id})

    def get_success_url(self):
        return reverse_lazy('without',)


class UpdateRatingView(LoginRequiredAndMethodistMixin, UpdateView):
    model = Rating
    form_class = RatingForm

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'update-rating': True})

    def get_success_url(self):
        return reverse_lazy('without',)


class AuthViews(LoginView):
    template_name = 'methodist/auth.html'
    form_class = AuthForm

    def get_success_url(self):
        # username = self.request.POST.get('username')
        # password = self.request.POST.get('password')
        # user = authenticate(username=username, password=password)
        # if self.request.user.is_superuser:
        #     login(self.request, user)
        #     return HttpResponseRedirect('/admin/')
        if self.request.user.group.name == 'Студент':
            return reverse_lazy('student-rating')
        elif self.request.user.group.name == 'Методист':
            return reverse_lazy('list-subjects')


class LogoutViews(LogoutView):
    next_page = 'auth'


class ProfileStudent(DetailView):
    template_name = 'methodist/student_profile.html'
    model = Student
    context_object_name = 'student'
    
    def get_queryset(self):
        return Student.objects.select_related('user')
    