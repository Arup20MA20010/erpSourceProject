# from django import forms
# from django.forms import ModelForm
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.core.validators import MinLengthValidator,MaxLengthValidator
# from erpApp.models import Department
# from .models import Communicate

# def getDepartmentChoice(Department):
#     departmentList=[]
#     departments=Department.objects.all()
#     for department in departments:
#         departmentList.append(department,department.departmentName)
#     return departmentList

# depChoice=getDepartmentChoice(Department)

# class FacultyRegistrationForm(UserCreationForm):
#     username=forms.CharField(max_length=150)
#     first_name=forms.CharField(max_length=100)
#     last_name=forms.CharField(max_length=100)
#     email=forms.EmailField()
#     department=forms.ChoiceField(choices=depChoice)
#     phone_no=forms.CharField(validators=[MinLengthValidator(10),MaxLengthValidator(10)])
#     class Meta:
#         model=User
#         fields=["username","first_name","last_name","email","phone_no","password1","password2"]

# class AnswerForm(ModelForm):
#     class Meta:
#         model=Communicate
#         fields=["answer","responded"]
