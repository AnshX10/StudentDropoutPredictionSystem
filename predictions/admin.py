# predictions/admin.py
from django.contrib import admin
from .models import PredictionReport

class PredictionReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_record', 'risk_level', 'risk_score', 'generated_at')
    list_filter = ('risk_level', 'generated_at')

admin.site.register(PredictionReport, PredictionReportAdmin)