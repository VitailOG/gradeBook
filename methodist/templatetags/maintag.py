from django import template
from ..models import Rating

register = template.Library()


@register.simple_tag
def get_current_semester(semester):
    return semester.split('/')[-1]


@register.simple_tag
def tag(user, subject, semester):
    return Rating.objects.filter(user__username=user, subject__name_subject=subject, semester=semester)\
        .values('id', 'user', 'rating_5', 'rating_12', 'retransmission',
                'credited', 'teacher', 'date_rating').first()


# refactoring
@register.simple_tag
def tag2(user, subject):
    return Rating.objects.filter(user__username=user, subject__name_subject=subject, semester__isnull=True)\
        .values('id', 'user', 'rating_5', 'rating_12', 'retransmission',
                'credited', 'teacher', 'date_rating').first()


# refactoring
@register.simple_tag
def get_rating_of_semesters(user, subject):
    return Rating.objects.filter(user__username=user, subject__name_subject=subject, semester__isnull=False) \
        .values('rating_5', 'rating_12')


@register.simple_tag
def get_list_semesters(initial_semester, final_semester):
    return [i for i in range(int(initial_semester), int(final_semester) + 1)]
