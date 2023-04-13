from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Department, Course, Enrollments
from users.models import Student
from django.urls import reverse
from .utilityFunctions import getAllEnrollmentsForGivenSemester, getCGPA, getInfoFromEnrollment, getInfoFromEnrollments, getAllEnrollmentsForGivenStudent, getSGPA, ifCouseTaken, getMaxSemesterRegistered, getSemeseterCourses
from .forms import SubjectRegistrationForm, SemRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View
# Create your views here.


def listDepartments(request):
    departments = Department.objects.all()
    print(departments)
    return render(request, "erpApp/listDepartments.html", {
        "departmentList": departments
    })

# detail of a single course


def courseDetail(request, courseName):
    isMe = False
    course = Course.objects.get(courseName=courseName)
    return render(request, "erpApp/course.html", {
        "courseName": course.courseName,
        "courseDetail": course.description,
        "courseCredits": course.credits_score,
        "isMe": isMe
    })

# def myCourseDetail(request,courseName):
#     isMe=True


def listCourses(request, deptName):
    isMyList = False
    department = Department.objects.get(departmentName=deptName)
    courseList = department.dept.all()
    return render(request, "erpApp/listCourses.html", {
        "courseList": courseList,
        "deptName": department.departmentName,
        "isMyList": isMyList
    })

# my courses


def myCourses(request, rollNo):
    # student=Student.objects.get(rollNo=rollNo)
    enrollmentList = getAllEnrollmentsForGivenStudent(rollNo)
    infoList = getInfoFromEnrollments(enrollmentList)
    return render(request, "erpApp/courseList.html", {
        "courseList": infoList,
        "checked": True
    })


def studentDashboardOverall(request, rollNo):
    maxSem = getMaxSemesterRegistered(rollNo)
    infoList = []
    for sem in range(1, maxSem+1):
        sgpa = getSGPA(rollNo, sem)
        infoList.append({
            "sem": sem,
            "sgpa": sgpa[0],
            "totalCredits": sgpa[1]
        })

    cgpa = getCGPA(rollNo, maxSem)
    return render(request, "erpApp/dashboard.html", {
        "infoList": infoList,
        "cgpa": cgpa[0],
        "totalCredit": cgpa[1]
    })


def studentDashboard(request, rollNo, semester):
    student = Student.objects.get(rollNo=rollNo)
    name = f"{student.firstName} {student.lastName}"
    enrollmentList = getAllEnrollmentsForGivenSemester(rollNo, semester)
    infoList = getInfoFromEnrollments(enrollmentList)
    sgpa = getSGPA(rollNo, semester)
    return render(request, "erpApp/dashboardSem.html", {
        "name": name,
        "sgpa": sgpa[0],
        "totalCredits": sgpa[1],
        "infoList": infoList,
        "semester": semester,
    })


class semRegister(View):
    subForm = False
    registerd = False

    def get(self, request, rollNo):
        semForm = SemRegistrationForm()
        showCourseList = False
        return render(request, "erpApp/semRegister.html", {
            "semForm": semForm,
            "subForm": self.subForm,
            "showCourseList": showCourseList,
            "registered": self.registerd
        })

    def post(self, request, rollNo):
        showCourseList = False
        courseList = []
        semForm = SemRegistrationForm(request.POST)
        if semForm.is_valid():
            semester = semForm.cleaned_data['semester']
            courseList = getSemeseterCourses(rollNo, semester)
            print(request.user)
            studentData = Student.objects.get(rollNo=rollNo)
            for courseData in courseList:
                enrollmentNew = Enrollments(
                    studentData=studentData, courseData=courseData)

                if (len(Enrollments.objects.filter(studentData=studentData, courseData=courseData)) == 0):
                    enrollmentNew.save()
            showCourseList = True
            self.registerd = True

            return render(request, "erpApp/courseList.html", {
                "semester": semester,
                "courseList": courseList,
                "registered": self.registerd,
                "checked": False
            })
        return render(request, "erpApp/semRegister.html", {
            "semForm": semForm,
            "subForm": self.subForm,
            "showCourseList": showCourseList,
            "courseList": courseList,
            "registred": self.registerd
        })


def subjectRegister(request, rollNo):
    subForm = True
    if request.method == 'POST':
        form = SubjectRegistrationForm(request.POST)
        courseName = request.POST['courseName']
        course = Course.objects.filter(courseName=courseName)
        semester = request.POST['semester']

        if len(course) > 0:
            course = course[0]
            credit = course.credits_score
            totalCredit = getSGPA(rollNo, semester)[1]
            if totalCredit+credit > 27:
                return render(request, "erpApp/subjectRegistration.html", {
                    "form": form,
                    "errorBool": True,
                    "errorMessage": "Total credit exceed 24,cannot register",
                    "subForm": subForm
                })
            if (ifCouseTaken(rollNo, courseName)):
                return render(request, "erpApp/subjectRegistration.html", {
                    "form": form,
                    "errorBool": True,
                    "errorMessage": "Course already taken",
                    "subForm": subForm
                })
            if (course.semester != int(semester)):
                return render(request, "erpApp/subjectRegistration.html", {
                    "form": form,
                    "errorBool": True,
                    "errorMessage": f"Course is not offered in the {semester} semester. It is offered in {course.semester} ",
                    "subForm": subForm
                })

        # if form is validated then only save to the database
        if form.is_valid():
            student = Student.objects.get(rollNo=rollNo)
            enrollment = Enrollments(studentData=student, courseData=course)
            enrollment.save()
            messages.success(
                request,
                "You have successfuly registered to the subject"
            )
            if not form.cleaned_data["addMore"]:
                redirectedUrl = reverse("dashboard", args=[rollNo, semester])
                return HttpResponseRedirect(redirectedUrl)
            else:
                form = SubjectRegistrationForm()
    else:
        form = SubjectRegistrationForm()

    return render(request, "erpApp/subjectRegistration.html", {
        "form": form,
        "errorBool": False,
        "subForm": subForm
    })
