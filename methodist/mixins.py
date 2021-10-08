from django.views.generic import DetailView

from .forms import StudentForm
from .models import Subject


class StudentMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StudentForm()
        return context


class AbstractRatingMixin(DetailView):
    model = Subject
    context_object_name = 'rating'
