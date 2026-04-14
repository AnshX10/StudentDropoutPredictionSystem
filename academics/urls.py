# academics/urls.py
from django.urls import path
from . import views

urlpatterns =[
    path('add-record/<int:student_id>/', views.add_academic_record, name='add_academic_record'),
]