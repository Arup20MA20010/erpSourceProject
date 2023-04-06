from django.urls import path
from . import views
urlpatterns = [
    path("departments", views.listDepartments, name="listDepartment"),
    path("<str:deptName>/courses", views.listCourses, name="listCourse"),
    path("<str:deptCode>/courses", views.listCoursesCode, name="listCourseCode")
]
