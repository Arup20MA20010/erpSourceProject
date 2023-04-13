from django.db import models
from erpApp.models import Department
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from users.models import Student
# Create your models here.


class Faculty(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, related_name="faculty")
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department, on_delete=models.DO_NOTHING, related_name="faculties")
    email_id = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Communicate(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="query")
    faculty = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, related_name="query")
    query = models.TextField(max_length=200, null=False)
    answer = models.TextField(max_length=200, null=True)
    responded = models.BooleanField(default=False)
