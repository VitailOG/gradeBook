from django import template
from ..models import Rating

register = template.Library()


@register.simple_tag
def get_current_semester(semester):
    print(semester.split('/')[-1])
    return semester.split('/')[-1]


@register.simple_tag
def tag(user, subject, semester):
    return Rating.objects.filter(user__username=user, subject__name_subject=subject, semester=semester)\
        .values('id', 'user', 'rating_5', 'rating_12', 'retransmission',
                'credited', 'teacher', 'date_rating').first()


@register.simple_tag
def get_list_semesters(initial_semester, final_semester):
    return [i for i in range(int(initial_semester), int(final_semester) + 1)]
