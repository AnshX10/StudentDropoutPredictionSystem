# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from academics.models import StudentProfile
from predictions.models import PredictionReport
from academics.models import AcademicRecord
from counseling.models import CounselingSession
from django.contrib.auth import get_user_model
from .decorators import allowed_users

# Use get_user_model to avoid circular imports and respect AUTH_USER_MODEL
User = get_user_model()

def login_view(request):
    # If user is already logged in, send them to their dashboard
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_based_on_role(user)
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Helper function to check role and redirect
def redirect_based_on_role(user):
    if user.is_superuser or user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif user.role == 'FACULTY':
        return redirect('faculty_dashboard')
    elif user.role == 'COUNSELOR':
        return redirect('counselor_dashboard')
    elif user.role == 'STUDENT':
        return redirect('student_dashboard')
    return redirect('login')

# --- DASHBOARD VIEWS ---
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        return redirect('login')

    # 1. User Counts
    total_students = StudentProfile.objects.count()
    total_faculty = User.objects.filter(role='FACULTY').count()
    total_counselors = User.objects.filter(role='COUNSELOR').count()

    # 2. Risk Distribution for Chart.js
    # We want to count how many students fall into each risk category
    risk_counts = PredictionReport.objects.values('risk_level').annotate(total=Count('risk_level'))
    
    # Format data for the chart [Low, Medium, High]
    chart_data = [0, 0, 0] # Default
    for entry in risk_counts:
        if entry['risk_level'] == 'LOW': chart_data[0] = entry['total']
        elif entry['risk_level'] == 'MEDIUM': chart_data[1] = entry['total']
        elif entry['risk_level'] == 'HIGH': chart_data[2] = entry['total']

    context = {
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_counselors': total_counselors,
        'chart_data': chart_data,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)

# accounts/views.py (Inside faculty_dashboard)
@login_required
@allowed_users(allowed_roles=['FACULTY'])
def faculty_dashboard(request):
    query = request.GET.get('q') # Get the search text from URL
    # Optimize queries: fetch related `user` and prefetch academic records and their prediction
    base_qs = StudentProfile.objects.select_related('user').prefetch_related('academic_records__predictionreport')

    if query:
        # Filter by name or enrollment number using a single optimized queryset
        students = base_qs.filter(Q(user__first_name__icontains=query) | Q(enrollment_number__icontains=query))
    else:
        students = base_qs.all()
    
    return render(request, 'dashboards/faculty_dashboard.html', {'students': students, 'query': query})

@login_required
def counselor_dashboard(request):
    if request.user.role != 'COUNSELOR':
        return redirect('login')
        
    # Fetch all prediction reports that are HIGH or MEDIUM risk, ordered by newest
    # Optimize by select_related to include the linked student user and academic record
    at_risk_reports = PredictionReport.objects.select_related('student__user', 'academic_record').filter(
        risk_level__in=['HIGH', 'MEDIUM']
    ).order_by('-generated_at')
    
    return render(request, 'dashboards/counselor_dashboard.html', {'reports': at_risk_reports})

@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('login')
    
    # 1. Get the student's profile
    # We use .get() because each Student user has exactly one StudentProfile
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        return render(request, 'dashboards/student_dashboard.html', {'error': 'Profile not found.'})

    # 2. Get academic history
    academic_history = AcademicRecord.objects.filter(student=student_profile).order_by('-semester')

    # 3. Get the latest prediction report
    latest_prediction = PredictionReport.objects.filter(student=student_profile).order_by('-generated_at').first()

    # 4. Get counseling notes
    counseling_notes = CounselingSession.objects.filter(student=student_profile).order_by('-session_date')

    context = {
        'student': student_profile,
        'records': academic_history,
        'prediction': latest_prediction,
        'sessions': counseling_notes,
    }
    return render(request, 'dashboards/student_dashboard.html', context)