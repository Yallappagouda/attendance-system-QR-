from django.contrib import admin
from .models import StaffProfile, StudentProfile, Course, AttendanceSession, AttendanceRecord

admin.site.register(StaffProfile)
admin.site.register(StudentProfile)
admin.site.register(Course)
admin.site.register(AttendanceSession)
admin.site.register(AttendanceRecord)