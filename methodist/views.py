from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import View

from .models import *
from .forms import SubjectsForm, StudentForm, RatingForm
from .filters import StudentFilter, filter_student
from .mixins import StudentMixin


class ListSubjectsView(ListView):
    """ List subject on department
    """
    model = Subject
    template_name = 'methodist/subject.html'
    context_object_name = 'subjects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # form for create new subject
        context['form'] = SubjectsForm()
        return context


class CreateSubjectsView(CreateView):
    model = Subject
    form_class = SubjectsForm
    success_url = reverse_lazy('list-subjects')

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'created_subject': True, "subject_id": form.instance.id})


class SemestersView(DetailView):
    template_name = 'methodist/semesters.html'
    model = Subject
    context_object_name = 'semesters'


class DeleteSubjectsView(DeleteView):
    model = Subject
    form_class = SubjectsForm
    success_url = reverse_lazy('list-subjects')

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'delete': True})


class UpdateSubjectsView(UpdateView):
    model = Subject
    form_class = SubjectsForm
    success_url = reverse_lazy('list-subjects')

    def form_valid(self, form):
        print(self.request.POST)
        super().form_valid(form)
        return JsonResponse({'update_subject': True})


class CreateStudentView(CreateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('without')

    def form_valid(self, form):
        form.instance.user_id = self.kwargs.get('pk')
        super().form_valid(form)
        return JsonResponse({'created_student': True})


class StudentWithOutGroupView(StudentMixin, ListView):
    model = CustomUser
    queryset = CustomUser.objects.exclude(student__year_entry__isnull=False).filter(group_id=1)
    template_name = 'methodist/without_group.html'
    context_object_name = 'students'


class StudentsView(StudentMixin, ListView):
    model = Student
    template_name = 'methodist/students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = StudentFilter(self.request.GET,
                           queryset=Student.objects.values('id', 'user__first_name', 'user__last_name',
                                                           'user__surname', 'year_entry',
                                                           'educational_program__name', 'group__name'))
        context['students'] = qs
        return context


class UpdateStudentView(UpdateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('list_student')

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'update': True})


class DeleteStudentView(DeleteView):
    model = Student
    success_url = reverse_lazy('list_student')

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'delete': True})


o = {
    'ordering': ''
}


class FilterStudentView(View):
    def get(self, request, *args, **kwargs):
        ord = self.request.GET.get('ordering')
        if o['ordering'] and o['ordering'] == ord:
            ord = '-' + ord
        o['ordering'] = ord
        qs = Student.objects.values('id', 'user__first_name', 'user__last_name',
                                    'user__surname', 'year_entry',
                                    'educational_program__name', 'group__name').order_by(ord if ord else 'id')

        qs = filter_student(self.request, qs)

        return JsonResponse({'students': list(qs)})


class RatingView(DetailView):
    model = Subject
    template_name = 'methodist/rating.html'
    context_object_name = 'rating'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RatingForm()
        return context


class CreateRatingView(CreateView):
    model = Rating
    form_class = RatingForm

    def form_valid(self, form):
        form.instance.user_id = self.kwargs.get('pk_user')
        form.instance.subject_id = self.kwargs.get('pk_subject')
        super().form_valid(form)
        return JsonResponse({'create': True, 'rating_id': form.instance.id})

    def get_success_url(self):
        return reverse_lazy('rating', args=(self.kwargs.get('pk_subject'), self.kwargs.get('semester')))


class UpdateRatingView(UpdateView):
    model = Rating
    form_class = RatingForm
    # success_url = reverse_lazy('list_subjects')

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'update-rating': True})

    # def get_success_url(self):
    #     return reverse_lazy('rating', args=(self.kwargs.get('pk_subject'), self.kwargs.get('semester')))
