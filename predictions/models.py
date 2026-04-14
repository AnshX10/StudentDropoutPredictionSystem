# predictions/models.py
from django.db import models
from academics.models import StudentProfile, AcademicRecord

class PredictionReport(models.Model):
    RISK_CHOICES = (
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
    )
    
    # Connects to the student
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='predictions')
    
    # Connects to the specific semester data used to generate this prediction
    academic_record = models.OneToOneField(AcademicRecord, on_delete=models.CASCADE)
    
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES)
    risk_score = models.FloatField(help_text="Probability score (e.g., 0.85 means 85% risk)")
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.enrollment_number} - {self.get_risk_level_display()} ({self.risk_score * 100}%)"