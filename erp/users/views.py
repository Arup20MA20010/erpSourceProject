from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Student
from erpApp.models import Department, Course
# Create your views here.


def home(request):

    return render(request, "users/home.html")


def userRegistration(request):
    # context = {"User": "Me"
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            studentName = request.POST['name']
            rollNo = request.POST['roll_no']
            studentData = Student(name=studentName, rollNo=rollNo)
            studentData.save()
            form.save()
            messages.success(
                request, "Your account has been create.You can login now")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    return render(request, 'users/registration.html', context)
