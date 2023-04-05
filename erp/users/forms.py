from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

keyWords = ['MA', 'EE', 'CS', 'GG', 'CH', 'EC']


def rollNoValidator(rollNo):
    if len(rollNo) != 9 or rollNo[2:4] not in keyWords:
        raise ValidationError(
            _('%(rollNo) is not a valid roll number'),
            params={"roll number": rollNo},
        )


class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    roll_no = forms.CharField(max_length=9, validators=[rollNoValidator])
    email = forms.EmailField(required=True)
    phone_no = forms.CharField(required=True, validators=[
        MaxLengthValidator(10), MinLengthValidator(10)])

    class Meta:
        model = User
        fields = ['username', 'name', 'roll_no', 'email',
                  'phone_no', 'password1', 'password2']
