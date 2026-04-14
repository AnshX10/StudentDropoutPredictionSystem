# academics/models.py
from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    # Links this profile to the CustomUser we created in Step 2
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})
    
    enrollment_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50, help_text="e.g., Computer Science, Mechanical")
    batch_year = models.IntegerField(help_text="Year of admission, e.g., 2023")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.enrollment_number}"

class AcademicRecord(models.Model):
    # One student can have multiple semesters, so we use ForeignKey
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="academic_records")
    
    semester = models.IntegerField(help_text="e.g., 1, 2, 3...")
    attendance_percentage = models.FloatField(help_text="Percentage out of 100")
    sgpa = models.FloatField(help_text="Semester Grade Point Average (0-10)")
    cgpa = models.FloatField(help_text="Cumulative Grade Point Average (0-10)")
    backlogs_current = models.IntegerField(default=0, help_text="Number of failed subjects in this semester")
    
    # Financial/Social factors often impact dropout rates (optional but great for ML)
    fee_dues = models.BooleanField(default=False, help_text="Does the student have pending fee dues?")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures a student can't have two records for the same semester
        unique_together = ('student', 'semester')

    def __str__(self):
        return f"{self.student.enrollment_number} - Sem {self.semester}"