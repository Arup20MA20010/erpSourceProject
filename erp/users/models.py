from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinLengthValidator
# Create your models here.


class Student(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.DO_NOTHING,related_name="student")
    rollNo = models.CharField(max_length=9)
    firstName=models.CharField(max_length=100)
    lastName=models.CharField(max_length=100)
    email=models.EmailField(max_length=100);
    phone=models.CharField(validators=[MinLengthValidator(10), MaxLengthValidator(10)])
    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class OTPModel(models.Model):
    PURPOSE_CHOICES = (
        ('verify_phone_number','verify_phone_number'),
        ('reset_password','reset_password')
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    valid_until = models.DateTimeField(help_text="The timestamp of the moment of expiry of the saved token.")
    purpose = models.CharField(max_length=255, null=True, blank=True, choices=PURPOSE_CHOICES)

    def __str__(self):
        return str(self.phone_number)