from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import PasswordInput

from .models import CustomUser, Subject, Student, Rating


class SubjectsForm(forms.ModelForm):

    teachers = forms.MultipleChoiceField(
        choices=[(i.id, i.username) for i in CustomUser.objects.filter(group__name="Викладач")]
    )

    class Meta:
        model = Subject
        fields = ('name_subject',
                  'group',
                  'hours',
                  'semester',
                  'final_semester',
                  'teachers',
                  'finally_subject',
                  'form_of_control',
                  'url_on_moodle'
                  )


class StudentForm(forms.ModelForm):
    year_entry = forms.DateField(widget=forms.TextInput(attrs={'type': 'date',
                                                               'style': 'border-bottom-right-radius: .25rem !important;'
                                                                        ' border-top-right-radius: .25rem !important; '
                                                                        'border: solid #ced4da 1px;'}))

    class Meta:
        model = Student
        fields = ('year_entry', 'group', 'educational_program')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('date_rating',
                  'rating_5',
                  'rating_12',
                  'retransmission',
                  'credited',
                  'teacher',
                  'semester'
                  )


class AuthForm(AuthenticationForm, forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введіть логін'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Введіть пароль'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
