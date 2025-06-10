from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),

    # Staff
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/create_session/', views.create_session, name='create_session'),
    path('staff/session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('staff/session/<int:session_id>/export/', views.export_attendance, name='export_attendance'),

    # Student
    path('student/login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('attendance/mark/<int:session_id>/', views.mark_attendance, name='mark_attendance'),

    # Logout
    path('logout/', views.logout_view, name='logout'),
    path('accounts/login/', views.student_login, name='accounts_login'),
    path('staff/login/', views.staff_login, name='staff_login'),
]