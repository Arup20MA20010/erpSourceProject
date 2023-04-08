from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Department, Course,Enrollments
from users.models import Student
from django.urls import reverse
from .utilityFunctions import getAllEnrollmentsForGivenSemester,getCGPA,getInfoFromEnrollment,getInfoFromEnrollments,getAllEnrollmentsForGivenStudent,getSGPA,ifCouseTaken,getMaxSemesterRegistered
from .forms import SubjectRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login
# Create your views here.


def listDepartments(request):
    departments = Department.objects.all()
    print(departments)
    return render(request, "erpApp/listDepartments.html", {
        "departmentList": departments
    })

# detail of a single course
def courseDetail(request,courseName):
    isMe=False
    course=Course.objects.get(courseName=courseName)
    return render(request,"erpApp/course.html",{
        "courseName":course.courseName,
        "courseDetail":course.description,
        "courseCredits":course.credits_score,
        "isMe":isMe
    })

# def myCourseDetail(request,courseName):
#     isMe=True
    


def listCourses(request, deptName):
    isMyList=False
    department = Department.objects.get(departmentName=deptName)
    courseList = department.dept.all()
    return render(request, "erpApp/listCourses.html", {
        "courseList": courseList,
        "deptName": department.departmentName,
        "isMyList":isMyList
    })

#my courses
def myCourses(request,rollNo):
    # student=Student.objects.get(rollNo=rollNo)
    enrollmentList=getAllEnrollmentsForGivenStudent(rollNo)
    infoList=getInfoFromEnrollments(enrollmentList)
    courses=[]
    for info in infoList:
        courses.append(info["course"])
    return render(request,"erpApp/listCourses.html",{
        "courseList":courses,
    })

def studentDashboardOverall(request,rollNo):
    maxSem=getMaxSemesterRegistered(rollNo)
    infoList=[]
    for sem in range(1,maxSem+1):
        sgpa=getSGPA(rollNo,sem)
        infoList.append({
            "sem":sem,
            "sgpa":sgpa[0],
            "totalCredits":sgpa[1]
        })
    
    cgpa=getCGPA(rollNo,maxSem)
    return render(request,"erpApp/dashboard.html",{
        "infoList":infoList,
        "cgpa":cgpa[0],
        "totalCredit":cgpa[1]
    })


def studentDashboard(request,rollNo,semester):
    student=Student.objects.get(rollNo=rollNo)
    name=f"{student.firstName} {student.lastName}"
    enrollmentList=getAllEnrollmentsForGivenSemester(rollNo,semester)
    infoList=getInfoFromEnrollments(enrollmentList)
    sgpa=getSGPA(rollNo,semester)
    return render(request,"erpApp/dashboardSem.html",{
        "name":name,
        "sgpa":sgpa[0],
        "totalCredits":sgpa[1],
        "infoList":infoList,
        "semester":semester,
    })

def  subjectRegister(request,rollNo):
    if request.method=='POST':
        form=SubjectRegistrationForm(request.POST)
        courseName=request.POST['courseName']
        course=Course.objects.filter(courseName=courseName)
        semester=request.POST['semester']

        if len(course)>0:
            course=course[0]
            credit=course.credits_score
            totalCredit=getSGPA(rollNo,semester)[1]
            if totalCredit+credit>24:
                return render(request,"erpApp/subjectRegistration.html",{
                    "form":form,
                    "errorBool":True,
                    "errorMessage":"Total credit exceed 24,cannot register"
                })
            if(ifCouseTaken(rollNo,courseName)):
                return render(request,"erpApp/subjectRegistration.html",{
                    "form":form,
                    "errorBool":True,
                    "errorMessage":"Course already taken"
                })
            if(course.semester!=int(semester)):
                return render(request,"erpApp/subjectRegistration.html",{
                    "form":form,
                    "errorBool":True,
                    "errorMessage":f"Course is not offered in the {semester} semester. It is offered in {course.semester} "
                })

        # if form is validated then only save to the database
        if form.is_valid():
            student=Student.objects.get(rollNo=rollNo)
            enrollment=Enrollments(studentData=student,courseData=course)
            enrollment.save()
            messages.success(
                request,
                "You have successfuly registered to the subject"
            )
            if not form.cleaned_data["addMore"]:
                redirectedUrl=reverse("dashboard",args=[rollNo,semester])
                return HttpResponseRedirect(redirectedUrl)
            else:
                form=SubjectRegistrationForm()
    else:
        form=SubjectRegistrationForm()
    
    return render(request,"erpApp/subjectRegistration.html",{
        "form":form,
        "errorBool":False,
    })
            

