# academics/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from .forms import AcademicRecordForm

@login_required
def add_academic_record(request, student_id):
    # Only faculty should add marks
    if request.user.role != 'FACULTY':
        return redirect('login')

    student = get_object_or_404(StudentProfile, id=student_id)

    if request.method == 'POST':
        form = AcademicRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.student = student # Link the record to this specific student
            record.save()
            return redirect('faculty_dashboard') # Go back to dashboard after saving
    else:
        form = AcademicRecordForm()

    return render(request, 'academics/add_record.html', {'form': form, 'student': student})