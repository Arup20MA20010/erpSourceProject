from .models import Enrollments,Course
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def courseValidation(courseName):
    if len(Course.objects.filter(courseName=courseName))==0:
        raise ValidationError(
            _("%(courseName) is not available. Please find some other course"),
            params={"courseName":courseName}
        )


class SubjectRegistrationForm(forms.Form):
    courseName=forms.CharField(max_length=100,required=True,validators=[courseValidation])
    addMore=forms.BooleanField()
