from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.http import HttpResponse
from .models import StaffProfile, StudentProfile, Course, AttendanceSession, AttendanceRecord
from .forms import AttendanceSessionForm
import qrcode
from io import BytesIO
import xlwt

def landing(request):
    return render(request, "attendance/landing.html")

def is_staff(user):
    return hasattr(user, 'staffprofile')

def is_student(user):
    return hasattr(user, 'studentprofile')

# ------------ Staff Views ------------

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    staff_profile = request.user.staffprofile
    sessions = AttendanceSession.objects.filter(created_by=staff_profile).order_by('-start_time')
    return render(request, 'attendance/staff_dashboard.html', {'sessions': sessions})

@login_required
@user_passes_test(is_staff)
def create_session(request):
    staff_profile = request.user.staffprofile
    if request.method == "POST":
        form = AttendanceSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = staff_profile
            session.save()
            # Generate QR code with session id
            server_ip = "192.168.249.146"  # <-- use your actual IP address here
            qr_url = f"http://{server_ip}:8000/attendance/mark/{session.id}/"
            buffer = BytesIO()
            qr_img = qrcode.make(qr_url)  
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            session.qr_code.save(f"session_{session.id}.png", buffer)
            session.save()
            return redirect('staff_dashboard')
    else:
        form = AttendanceSessionForm()
        form.fields['course'].queryset = Course.objects.filter(staff=staff_profile)
    return render(request, 'attendance/create_session.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def session_detail(request, session_id):
    session = get_object_or_404(AttendanceSession, id=session_id, created_by=request.user.staffprofile)
    records = AttendanceRecord.objects.filter(session=session).select_related('student__user')
    return render(request, 'attendance/session_detail.html', {'session': session, 'records': records})

@login_required
@user_passes_test(is_staff)
def export_attendance(request, session_id):
    session = get_object_or_404(AttendanceSession, id=session_id, created_by=request.user.staffprofile)
    records = AttendanceRecord.objects.filter(session=session).select_related('student__user')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="attendance_{session.course.name}_{session.id}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Attendance')
    ws.write(0, 0, 'Student Name')
    ws.write(0, 1, 'Student ID')
    ws.write(0, 2, 'Timestamp')
    for row, rec in enumerate(records, start=1):
        ws.write(row, 0, rec.student.user.get_full_name())
        ws.write(row, 1, rec.student.student_id)
        ws.write(row, 2, rec.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
    wb.save(response)
    return response

# ------------ Student Views ------------

def student_login(request):
    msg = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and is_student(user):
            login(request, user)
            return redirect("student_dashboard")
        else:
            msg = "Invalid credentials or not student!"
    return render(request, "attendance/student_login.html", {"msg": msg})

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student_profile = request.user.studentprofile
    # Show only sessions within last 2 hours
    now = timezone.now()
    sessions = AttendanceSession.objects.filter(
        start_time__gte=now - timezone.timedelta(hours=2),
        is_active=True
    )
    return render(request, 'attendance/student_dashboard.html', {'sessions': sessions})

@login_required
@user_passes_test(is_student)
def mark_attendance(request, session_id):
    session = get_object_or_404(AttendanceSession, id=session_id, is_active=True)
    if not session.is_within_2_hours:
        return render(request, "attendance/attendance_failed.html", {"reason": "Session expired"})
    student_profile = request.user.studentprofile
    already_marked = AttendanceRecord.objects.filter(session=session, student=student_profile).exists()
    if not already_marked:
        AttendanceRecord.objects.create(session=session, student=student_profile)
    return render(request, "attendance/attendance_marked.html", {
        "session": session,
        "student": student_profile,
        "already_marked": already_marked
    })
def staff_login(request):
    msg = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        # Check staff profile
        if user and hasattr(user, 'staffprofile'):
            login(request, user)
            return redirect("staff_dashboard")
        else:
            msg = "Invalid credentials or not staff!"
    return render(request, "attendance/staff_login.html", {"msg": msg})

def logout_view(request):
    logout(request)
    return redirect('landing')