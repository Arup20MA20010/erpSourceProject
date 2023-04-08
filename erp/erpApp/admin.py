from django.contrib import admin

# Register your models here.
from .models import Course, Department, Enrollments

admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Enrollments)
