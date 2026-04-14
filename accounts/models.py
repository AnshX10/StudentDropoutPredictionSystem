# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Define the 4 distinct roles
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('FACULTY', 'Faculty'),
        ('COUNSELOR', 'Counselor'),
        ('STUDENT', 'Student'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    # Helper properties to easily check user roles in HTML templates later
    @property
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser

    @property
    def is_faculty(self):
        return self.role == 'FACULTY'

    @property
    def is_counselor(self):
        return self.role == 'COUNSELOR'

    @property
    def is_student(self):
        return self.role == 'STUDENT'