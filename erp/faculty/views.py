from django.shortcuts import render
from .models import Faculty, Communicate
from .forms import FacultyRegistrationForm, AnswerForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.views import View
# Create your views here.


class FacultyReg(View):

    def get(request):
        form = FacultyRegistrationForm()
        return render(request, "faculty/registration.html", {
            "form": form
        })

    def post(request):
        form = FacultyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            department = form.cleaned_data['department']
            firstName = form.cleaned_data['first_name']
            lastName = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            faculty = Faculty(user=user, department=department,
                              firstName=firstName, lastName=lastName, email=email)
            faculty.save()
            return HttpResponseRedirect('dummy')

        return render(request, "faculty/registration.html", {
            "form": form
        })


class Answer(View):
    def get(request):
        form = AnswerForm()
        faculty = request.user.faculty
        queries = Communicate.objects.filter(faculty=faculty)

        return render(request, "base.html", {
            "form": form,
            "queries": queries
        })

    def post(request):
        form = AnswerForm(request.POST)
        faculty = request.user.faculty
        queries = Communicate.objects.filter(faculty=faculty)
        if form.valid():
            form.save()
        return render(request, "base.html", {
            "form": form,
            "queries": queries
        })
