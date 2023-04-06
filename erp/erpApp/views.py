from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Department, Course
from django.urls import reverse
# Create your views here.


def listDepartments(request):
    departments = Department.objects.all()
    print(departments)
    return render(request, "erpApp/listDepartments.html", {
        "departmentList": departments
    })


def listCourses(request, deptName):
    department = Department.objects.get(departmentName=deptName)
    courseList = department.dept.all()
    return render(request, "erpApp/listCourses.html", {
        "courseList": courseList,
        "deptName": department.departmentName,
    })


def listCoursesCode(request, deptCode):
    department = Department.objects.get(depCode=deptCode)
    deptName = department.departmentName
    redirectedUrl = reverse("listCourse", args=[deptName])
    return HttpResponseRedirect(redirectedUrl)
