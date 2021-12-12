from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from methodist.models import Rating


class StudentRatingBySemestersView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'student/student_rating.html')


class StudentRatingBySemesterView(View):

    def get(self, request, *args, **kwargs):
        print(request.GET.get('student_id'))
        student_ratings = Rating.objects.filter(
            semester=self.kwargs.get('pk'),
            user_id=request.GET.get('student_id')
        ).select_related(
            'subject'
        ).values(
            'subject__name_subject',
            'rating_5',
            'rating_12',
            'retransmission',
            'credited',
            'date_rating',
            'teacher__last_name',
            'teacher__first_name',
            'teacher__surname'
        )
        return JsonResponse({'s': list(student_ratings)})
