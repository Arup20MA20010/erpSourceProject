from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def register(request):
    pass


def login(request):
    pass


def User(request):
    return HttpResponse("User")


def Student(request):
    return HttpResponse('Student')


def Professor(request):
    return HttpResponse('Professor')
