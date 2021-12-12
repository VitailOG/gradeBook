from django import template
from methodist.models import Rating

register = template.Library()


@register.simple_tag
def get_all_semesters_student(student_id):
    semesters = Rating.objects.filter(
        user_id=student_id,
        semester__isnull=False
    ).order_by(
        'semester'
    ).values(
        'semester'
    ).distinct()
    return semesters
