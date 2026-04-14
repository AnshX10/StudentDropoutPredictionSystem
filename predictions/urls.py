# predictions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('predict/<int:record_id>/', views.generate_prediction, name='generate_prediction'),
    # Download PDF report for a student
    path('download/<int:student_id>/', views.export_student_report, name='download_report'),
]