from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm, QueryForm
from django.template.loader import render_to_string
from .models import Student,OTPModel
from django.views import View
from faculty.models import Communicate
from django.utils.encoding import force_bytes,force_str
from .utilityFun import generate_token
from django.conf import settings
import random
from twilio.rest import Client
import datetime

import time


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
            email=request.POST['email']
            phone=request.POST['phone']
            try:

                if(Student.objects.get(email=email)):
                    messages.info(request,"This account already exists.")
                    return render(request,"signup.html")
                # return HttpResponse("Email already exists")
            except Exception as e:
                print(e)
            
            studentData = Student(
                user=user, firstName=studentFirstName, lastName=studentLastName, rollNo=rollNo,email=email,phone_no=phone)
            studentData.is_active=False;
            email_subject="email account activation link"
            message=render_to_string('activate.html',{
                'user':user,
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user)
            })
            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        try:
            email_message.send()
        except Exception as e:
            print(e)
            messages.warning(request,e)
            user.delete()
            return render(request,"signup.html")
        messages.success(request,"Acount Activation Link Has been Sent. Check your gmail")
        # return redirect('/auth/login')
        return render(request,'users/registration.html', context)
        
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    return render(request, 'users/registration.html', context)

class ActivateAccount(View):
     def get(self,request,uidb64,token):
        try:
            #uid is the primary key as I am decoding the encoded primary key
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=Student.objects.get(pk=uid)
        except Exception as e:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account Created Successfuly. Happy Shopping")
            return redirect('/login/')
        return render(request,'activationFailed.html')

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

class Query(View):
    def get(request):
        form=QueryForm()
        return render(request,"base.html",{
            "form":form
        })

    def post(request):
        form=QueryForm(request.POST)
        if form.is_valid():
            query=form.cleaned_data['query']
            faculty=form.cleaned_data['faculty']
            student=request.user.student
            communicate=Communicate(student=student,faculty=faculty,query=query)
            communicate.save()

        return render(request,"base.html",{
            "form":form
        })


def send_otp(request):
    try:
        if "phone_number" not in request.data:
            return render(request,"phone_number_not_found.html");
        if "purpose" not in request.data:
            return render(request,"purposeMissing.html");
        phone_number=request.POST['phone_number']
        purpose=request.POST['purpose']
        account_sid = settings.ACCOUNTS_SID
        auth_token = settings.AUTH_TOKEN
        client = Client(account_sid, auth_token)
        otp = random.randint(100000, 999999)
        message = client.messages.create(body="Hello, Your OTP is " +
                                         str(otp),
                                         from_=settings.PHONE,
                                         to='+91' + phone_number)
        otp_obj = OTPModel.objects.filter(phone_number=phone_number).filter(purpose=purpose).first()
        if otp_obj is not None:
            otp_obj.delete()
        otp_obj = OTPModel.objects.create(otp=otp, phone_number=phone_number, purpose=purpose,valid_until=timezone.now()+datetime.timedelta(seconds=settings.OTP_EXPIRY_TIME))
        otp_obj.save()
        return render()
    except Exception as e:
        print(e);

def verify_otp(request):
    if "phone_number" not in request.data:
        return render(request,"Error.html",{"error":"Phone number missing"})
        
    if "otp" not in request.data:
        return render(request,"Error.html",{"error":"OTP missing"})
        
    if "purpose" not in request.data:
        return render(request,"Error.html",{"error":"Purpose missing"})

    phone_number = request.data["phone_number"]
    user_otp = request.data['otp']
    purpose = request.data['purpose']

    otp_obj = OTPModel.objects.filter(phone_number=phone_number).filter(purpose=purpose).first()
       
    if otp_obj is None:
        return render(request,{"error":"No OTP is sent on this phone number with the specified purpose"})

    if not user_otp:
        return render(request,{'error': 'User OTP is missing'})

    if str(user_otp) != str(otp_obj.otp):
        return render(request,{'error': 'Invalid OTP'},)
        
    if otp_obj.valid_until < timezone.now():
        return render(request,{'error': 'OTP has expired'})
        
    otp_obj.delete()
    return redirect('/login')
