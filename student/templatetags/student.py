from django import template
from methodist.models import Rating

register = template.Library()


@register.simple_tag
def get_all_semesters_student(student):
    print(student)
    semesters = Rating.objects.filter(
        user=student,
        semester__isnull=False
    ).order_by(
        'semester'
    ).values(
        'semester'
    ).distinct()
    print(semesters)
    return semesters
