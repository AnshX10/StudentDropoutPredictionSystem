# accounts/urls.py
from django.urls import path
from . import views

urlpatterns =[
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('counselor-dashboard/', views.counselor_dashboard, name='counselor_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
]