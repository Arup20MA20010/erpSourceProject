from django.urls import path
from . import views

urlpatterns = [
    path('facultyRegistration', views.FacultyReg.as_view(), name="facReg")
]
