from django.urls import path
from .views import *

urlpatterns = [
    path('subject/', ListSubjectsView.as_view(), name="list-subjects"),
    path('create-subjects/', CreateSubjectsView.as_view(), name="create_subjects"),
    path('delete/<int:pk>', DeleteSubjectsView.as_view(), name="delete_subject"),
    path('update/<int:pk>', UpdateSubjectsView.as_view(), name="update_subject"),
    path('semesters/<int:pk>', SemestersView.as_view(), name="semesters"),

    path('without-group/', StudentWithOutGroupView.as_view(), name="without"),
    path('add-student/<int:pk>', CreateStudentView.as_view(), name="create-student"),
    path('student/', StudentsView.as_view(), name="list_student"),
    path('update-student/<int:pk>', UpdateStudentView.as_view(), name="update-student"),
    path('delete-student/<int:pk>', DeleteStudentView.as_view(), name="delete-student"),
    path('filter-student/', FilterStudentView.as_view(), name="filter-student"),
    path('student-profile/<int:pk>', ProfileStudent.as_view(), name="student-profile"),

    path('rating/<int:pk>/<int:semester>', RatingView.as_view(), name="rating"),
    path('rating-year/<int:pk>', RatingYearView.as_view(), name="rating-year"),
    path('create-rating/<int:pk_subject>/<int:pk_user>', CreateRatingView.as_view(), name="create"),
    path('update-rating/<int:pk>', UpdateRatingView.as_view(), name="update"),

    path('', AuthViews.as_view(), name='auth'),
    path('logout/', LogoutViews.as_view(), name="logout")
]
