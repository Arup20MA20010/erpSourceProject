from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
# Create your models here.
# class User(models.Model):
#     pass


class Student(models.Model):
    name = models.CharField(max_length=100)
    rollNo = models.CharField(max_length=11)
    phone_number = models.IntegerField(
        validators=[MaxLengthValidator(10), MinLengthValidator(10)])
