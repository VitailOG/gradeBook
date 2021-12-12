from .models import CustomUser, EducationalProgram, Group


def get_teachers(request):
    teachers = CustomUser.objects.filter(group__name="Викладач")
    return {"teachers": teachers}


def get_group(request):
    if request.user.is_authenticated:
        group = Group.objects.filter(department=request.user.department)
        return {"group": group}
    return {"group": []}


def none(request):
    return {'none': None}
