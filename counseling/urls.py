# counseling/urls.py
from django.urls import path
from . import views

urlpatterns =[
    path('add-note/<int:student_id>/', views.add_counseling_note, name='add_counseling_note'),
]