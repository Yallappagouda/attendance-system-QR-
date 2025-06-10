from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.staff_id})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='courses')
    def __str__(self):
        return f"{self.name} ({self.code})"

class AttendanceSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_by = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='session_qrcodes/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def is_within_2_hours(self):
        return timezone.now() <= self.start_time + timezone.timedelta(hours=2)
    def __str__(self):
        return f"{self.course.name} | {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class AttendanceRecord(models.Model):
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('session', 'student')
    def __str__(self):
        return f"{self.student.user.get_full_name()} | {self.session}"