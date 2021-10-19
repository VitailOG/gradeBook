from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from methodist.models import Rating


class StudentRatingBySemestersView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'student/student_rating.html')


class StudentRatingBySemesterView(View):

    def get(self, request, *args, **kwargs):
        print(self.kwargs.get('pk'))

        student_ratings = Rating.objects.filter(
            semester=self.kwargs.get('pk'),
            user=self.request.user
        ).select_related(
            'subject'
        ).values(
            'subject__name_subject',
            'rating_5',
            'rating_12',
            'retransmission',
            'credited',
        )
        return JsonResponse({'s': list(student_ratings)})
