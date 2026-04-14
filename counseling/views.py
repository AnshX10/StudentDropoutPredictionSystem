# counseling/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from academics.models import StudentProfile
from .models import CounselingSession
from .forms import CounselingSessionForm

@login_required
def add_counseling_note(request, student_id):
    if request.user.role != 'COUNSELOR':
        return redirect('login')

    student = get_object_or_404(StudentProfile, id=student_id)
    # Fetch previous sessions to show the counselor the history
    previous_sessions = CounselingSession.objects.filter(student=student).order_by('-session_date')

    if request.method == 'POST':
        form = CounselingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.student = student
            session.counselor = request.user # Set the counselor to the logged-in user
            session.save()
            return redirect('counselor_dashboard')
    else:
        form = CounselingSessionForm()

    context = {
        'form': form,
        'student': student,
        'previous_sessions': previous_sessions
    }
    return render(request, 'counseling/add_note.html', context)