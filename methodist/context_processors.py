from .models import CustomUser, EducationalProgram, Group


def get_teachers(request):
    teachers = CustomUser.objects.filter(group__name="Викладач")
    return {"teachers": teachers}


def get_educational_program(request):
    group = Group.objects.all()
    return {"group": group}
