from django.db import models
from erpApp.models import Course
# Create your models here.


class Student(models.Model):
    rollNo = models.CharField(max_length=9)
    name = models.CharField(max_length=100)
    CourseId = models.ManyToManyField(
        Course, related_name="students")

    def __str__(self):
        return f"{self.name}"
