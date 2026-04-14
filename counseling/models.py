# counseling/models.py
from django.db import models
from django.conf import settings
from academics.models import StudentProfile

class CounselingSession(models.Model):
    PROGRESS_CHOICES = (
        ('WORSENING', 'Worsening'),
        ('NO_CHANGE', 'No Change'),
        ('IMPROVING', 'Improving'),
        ('RESOLVED', 'Risk Resolved'),
    )

    # The student being counseled
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='counseling_sessions')
    
    # The counselor conducting the session (Only users with 'COUNSELOR' role)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'COUNSELOR'})
    
    session_date = models.DateField()
    notes = models.TextField(help_text="Observation, discussion points, and planned actions.")
    progress_status = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='NO_CHANGE')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session: {self.student.enrollment_number} on {self.session_date}"