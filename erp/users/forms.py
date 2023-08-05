from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Faculty
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from erpApp.utilityFunctions import getFacultyList
from erpApp.constants import keyWords
# from faculty.models import Communicate, Faculty


def rollNoValidator(rollNo):
    if len(rollNo) != 9 or rollNo[2:4] not in keyWords:
        raise ValidationError(
            _('%(rollNo) is not a valid roll number'),
            params={"roll number": rollNo},
        )


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    roll_no = forms.CharField(max_length=9, validators=[rollNoValidator])
    email = forms.EmailField(required=True)
    phone_no = forms.CharField(required=True, validators=[
        MaxLengthValidator(10), MinLengthValidator(10)])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'roll_no', 'email',
                  'phone_no', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class QueryForm(forms.Form):
    faculty = forms.ChoiceField(choices=getFacultyList(Faculty))
    query = forms.CharField(widget=forms.Textarea)
