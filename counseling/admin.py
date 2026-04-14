# counseling/admin.py
from django.contrib import admin
from .models import CounselingSession

class CounselingSessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'counselor', 'session_date', 'progress_status')
    list_filter = ('progress_status', 'session_date')

admin.site.register(CounselingSession, CounselingSessionAdmin)