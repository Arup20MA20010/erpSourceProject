from django.urls import path
from . import views
urlpatterns = [
    path("departments", views.listDepartments, name="listDepartment"),
    path("dashboard/<str:rollNo>",
         views.studentDashboardOverall, name="dashboardOverall"),
    path("courses/<str:courseName>", views.courseDetail, name="course"),
    path("<str:deptName>/courses", views.listCourses, name="listCourse"),
    path("dashboard/courses/<str:rollNo>",
         views.myCourses, name="listMyCourse"),
    path("dashboard/<str:rollNo>/<int:semester>",
         views.studentDashboard, name="dashboard"),
    path("subject-registration/<str:rollNo>",
         views.subjectRegister, name="subjectRegistration"),
    path("sem-register/<str:rollNo>",
         views.semRegister.as_view(), name="semRegister")
]
