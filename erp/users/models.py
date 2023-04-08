from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Student(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.DO_NOTHING,related_name="student")
    rollNo = models.CharField(max_length=9)
    firstName=models.CharField(max_length=100)
    lastName=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
