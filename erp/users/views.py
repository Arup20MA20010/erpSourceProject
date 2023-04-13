from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from .models import Student
from django.views import View
# from faculty.models import Communicate
# Create your views here.


def home(request):

    return render(request, "users/home.html")


def userRegistration(request):
    # context = {"User": "Me"
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            studentFirstName = request.POST['first_name']
            studentLastName = request.POST['last_name']
            rollNo = request.POST['roll_no']
            password = form.cleaned_data.get("password1")
            print(password)
            username = form.cleaned_data.get("username")
            print(username)
            user = authenticate(username=username, password=password)
            print(user)
            studentData = Student(
                user=user, firstName=studentFirstName, lastName=studentLastName, rollNo=rollNo)
            studentData.save()
            messages.success(
                request, "Your account has been create.You can login now")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    return render(request, 'users/registration.html', context)


def loginView(request):
    messageBool = False
    message = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(
                    request, "You are logged in"
                )
                return redirect('home')
            else:
                message = "LoggedIn failed, Either of the password or username is wrong"
                messageBool = True

    else:
        form = LoginForm()

    return render(request, "users/login.html", {
        "form": form,
        "messageBool": messageBool,
        "message": message
    })


def logoutView(request):
    logout(request)
    messages.info(request, "You have successfuly logged out")
    return render(request, "users/logout.html")

# class Query(View):
#     def get(request):
#         form=QueryForm()
#         return render(request,"base.html",{
#             "form":form
#         })

#     def post(request):
#         form=QueryForm(request.POST)
#         if form.is_valid():
#             query=form.cleaned_data['query']
#             faculty=form.cleaned_data['faculty']
#             student=request.user.student
#             communicate=Communicate(student=student,faculty=faculty,query=query)
#             communicate.save()

#         return render(request,"base.html",{
#             "form":form
#         })


# def logout_user(request):
