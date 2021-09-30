from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Department(models.Model):
    """ Model Department
    """
    name = models.CharField(verbose_name="Назва відділення", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Відділ"
        verbose_name_plural = "Відділи"


class Permissions(models.Model):
    """ Add permissions for users
    """
    name = models.CharField(verbose_name="Право доступу", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Право доступу"
        verbose_name_plural = "Права доступу"


class Group(models.Model):
    """Add group
    """
    name = models.CharField(verbose_name="Назва групи", max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Група"
        verbose_name_plural = "Групи"


class CustomUser(AbstractUser):
    """ Extend model `User`
    """
    surname = models.CharField(verbose_name='По батькові', max_length=50)
    group = models.ForeignKey(Permissions, on_delete=models.CASCADE, verbose_name='Права доступу', blank=True,
                              null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Відділ', blank=True, null=True)

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"


class Student(models.Model):
    """ Model for students
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student')
    year_entry = models.DateField(verbose_name="Рік вступу", null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Група", null=True, blank=True)
    educational_program = models.ForeignKey('EducationalProgram', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенти"


class EducationalProgram(models.Model):
    """Освітні програми"""
    name = models.CharField(verbose_name="Назва освіт. програми", max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Відділення")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Освітня програма"
        verbose_name_plural = "Освітні програми"


class Subject(models.Model):

    CHOICES_SEMESTER = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
        ('6', 6),
        ('7', 7),
        ('8', 8)
    )

    CHOICES_CONTROL = (('Залік', 'Залік'), ('Екзамен', 'Екзамен'))

    name_subject = models.CharField(verbose_name="Назва предмета", max_length=60)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Група", null=True)
    teachers = models.ManyToManyField(CustomUser, verbose_name="Викладачі")
    hours = models.PositiveIntegerField(verbose_name="Кількість годин")
    loans = models.PositiveIntegerField(verbose_name="Кількість кредитів", blank=True)
    semester = models.CharField(verbose_name="Семестр", max_length=20, choices=CHOICES_SEMESTER)
    final_semester = models.CharField(verbose_name="Кінцевий семестр", max_length=20,
                                      null=True, blank=True, choices=CHOICES_SEMESTER)
    form_of_control = models.CharField(verbose_name="Форма конролю", max_length=20, choices=CHOICES_CONTROL)
    url_on_moodle = models.URLField()
    finally_subject = models.BooleanField(default=False)

    def __str__(self):
        return self.name_subject

    def save(self, *args, **kwargs):
        self.loans = self.hours // 2
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Студент")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    date_rating = models.DateField(verbose_name="Дата оцінки")
    rating_5 = models.PositiveIntegerField(verbose_name="Оцінка 5", null=True, blank=True)
    rating_12 = models.PositiveIntegerField(verbose_name="Оцінка 12", null=True, blank=True)
    retransmission = models.BooleanField(verbose_name="Перездача", default=False)
    credited = models.BooleanField(verbose_name="Зараховано", default=False)
    semester = models.PositiveIntegerField(verbose_name="Семестер", null=True, blank=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="teacher", null=True)

    def __str__(self):
        return f"{self.user.surname} оцінка {self.rating_5} з {self.subject.name_subject}"

    def save(self, *args, **kwargs):
        dict_rating = {
            (1, 2, 3): 2,
            (4, 5, 6): 3,
            (7, 8, 9): 4,
            (10, 11, 12): 5
        }
        if self.rating_12 is not None:
            for i in dict_rating.keys():
                if self.rating_12 in i:
                    self.rating_5 = dict_rating.get(i)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('rating', args=(self.subject.id,))

    class Meta:
        verbose_name = "Оцінка"
        verbose_name_plural = "Оцінки"
