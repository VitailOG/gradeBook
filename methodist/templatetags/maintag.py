from django import template
from ..models import Rating

register = template.Library()


@register.simple_tag
def get_current_semester(semester) -> int:
    return semester.split('/')[-1]


@register.simple_tag
def tag(subject, semester):

    rating_list = Rating.objects.filter(
        subject__name_subject=subject,
        semester=semester
    ).select_related(
        'user',
        'subject',
        'teacher'
    )

    return {i.user.id: i for i in rating_list}


@register.simple_tag
def get_rating(id: int, ratings: dict) -> dict:
    return ratings[id]


@register.simple_tag
def tag2(subject):
    ratings = Rating.objects.filter(
        subject__name_subject=subject,
        semester__isnull=True
    ).select_related(
        'user',
        'subject',
        'teacher'
    )
    return {i.user.id: i for i in ratings}


@register.simple_tag
def get_rating_of_semesters(subject):
    group_ratings_for_semesters = Rating.objects.filter(
        subject__name_subject=subject,
        semester__isnull=False
    ).select_related(
        'user'
    ).values(
        'rating_5',
        'user__username',
        'semester'
    ).order_by(
        'semester'
    )
    return group_ratings_for_semesters


@register.simple_tag
def get_user_ratings_for_semesters(user, ratings):
    return [i.get('rating_5') for i in ratings if i.get('user__username') == user]


@register.simple_tag
def get_list_semesters(initial_semester, final_semester):
    return [i for i in range(int(initial_semester), int(final_semester) + 1)]
