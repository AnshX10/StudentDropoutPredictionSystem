# predictions/views.py
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa

# Local models
from academics.models import StudentProfile
from .models import PredictionReport


def export_student_report(request, student_id):
    """Generate a PDF report for the given student and return as attachment.

    Uses `predictions/report_pdf.html` template. If the template or data
    are missing, the view will still return a (possibly empty) PDF response.
    """
    student = get_object_or_404(StudentProfile, id=student_id)
    records = student.academic_records.all()
    prediction = student.predictions.order_by('-generated_at').first()

    template_path = 'predictions/report_pdf.html'
    context = {'student': student, 'records': records, 'prediction': prediction}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Report_{student.enrollment_number}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # Create the PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # If an error happened, we still return the response (pisa writes error info into it)
    return response


def generate_prediction(request, record_id):
    """Generate a prediction for an AcademicRecord and save a PredictionReport.

    This is a lightweight rule-based fallback used when a ML model isn't
    available; it ensures the URL referenced by templates works.
    """
    from academics.models import AcademicRecord
    from django.shortcuts import redirect

    # Only accept POST requests from the faculty UI
    if request.method != 'POST':
        return redirect('faculty_dashboard')

    record = get_object_or_404(AcademicRecord, id=record_id)
    student = record.student

    # Simple heuristic for risk_level and score
    score = 0.0
    # attendance (0-100), sgpa (0-10), cgpa (0-10), backlogs (int)
    try:
        attendance = float(getattr(record, 'attendance_percentage', 0))
    except Exception:
        attendance = 0.0
    try:
        sgpa = float(getattr(record, 'sgpa', 0))
    except Exception:
        sgpa = 0.0
    backlogs = int(getattr(record, 'backlogs_current', getattr(record, 'backlogs', 0)))

    # Weighted simple score (higher means more risk)
    score = max(0.0, 1.0 - (sgpa / 10.0)) * 0.6 + min(1.0, backlogs / 5.0) * 0.4

    if sgpa < 5 or backlogs >= 4 or attendance < 50:
        risk_level = 'HIGH'
    elif sgpa < 7 or backlogs >= 2 or attendance < 75:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'

    # Create or update a PredictionReport tied to this academic record
    report = PredictionReport.objects.create(
        student=student,
        academic_record=record,
        risk_level=risk_level,
        risk_score=round(score, 3),
    )

    return redirect('faculty_dashboard')