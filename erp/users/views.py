from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm
# Create your views here.


def userRegistration(request):
    # context = {"User": "Me"
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been create.You can login now")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    return render(request, 'users/registration.html', context)
