from django.db import models
from django.core.validators import  MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from users.models import Student
# Create your models here.
# class User(models.Model):
#     pass
keyWords = ['MA', 'EE', 'CS', 'GG', 'CH', 'EC', 'ME','HS']


def depError(depCode):
    if depCode not in keyWords:
        raise ValidationError(
            _("%(depCode) is not a valid department code"),
            params={"depCode": depCode}
        )


class Department(models.Model):
    departmentName = models.CharField(max_length=100)
    facId = models.IntegerField()
    depCode = models.CharField(max_length=2, validators=[depError])

    def __str__(self):
        return self.departmentName


class Course(models.Model):
    courseName = models.CharField(max_length=50)
    credits_score = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    deptId = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="dept")
    
    semester=models.IntegerField(null=True)
    description=models.TextField(null=True)
    def __str__(self):
        return f"{self.courseName}"

class Enrollments(models.Model):
    courseData=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="enrollments")
    studentData=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="enrollments")
    grade=models.CharField(max_length=2,null=True)