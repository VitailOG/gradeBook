from django.urls import path
from .views import StudentRatingBySemestersView, StudentRatingBySemesterView


urlpatterns = [
    path('my-rating', StudentRatingBySemestersView.as_view(), name="student-rating"),
    path('rating-by-semester/<int:pk>', StudentRatingBySemesterView.as_view(), name="student-rating"),
]
