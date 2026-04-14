from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import StudentProfile, AcademicRecord

class AcademicRecordInline(TabularInline): # Modern inline
    model = AcademicRecord
    extra = 1

@admin.register(StudentProfile)
class StudentProfileAdmin(ModelAdmin): # Use Unfold ModelAdmin
    inlines = [AcademicRecordInline]
    list_display = ('user', 'enrollment_number', 'department')

@admin.register(AcademicRecord)
class AcademicRecordAdmin(ModelAdmin):
    pass