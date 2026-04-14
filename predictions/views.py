# predictions/views.py
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.conf import settings

# Local models
from academics.models import StudentProfile
from .models import PredictionReport

import pdfkit


def export_student_report(request, student_id):
    """Generate a PDF report for the given student and return as attachment.

    Uses `wkhtmltopdf` via `pdfkit` on Windows for better CSS support. If
    wkhtmltopdf isn't available or fails, falls back to xhtml2pdf to avoid
    breaking the endpoint entirely.
    """
    student = get_object_or_404(StudentProfile, id=student_id)
    records = student.academic_records.all()
    prediction = student.predictions.order_by('-generated_at').first()

    template_path = 'predictions/report_pdf.html'
    context = {'student': student, 'records': records, 'prediction': prediction}

    html = render_to_string(template_path, context, request=request)

    filename = f'Report_{student.enrollment_number}.pdf'

    # Try wkhtmltopdf via pdfkit (better CSS rendering). If it fails, fallback to xhtml2pdf.
    options = {
        'enable-local-file-access': None,  # allow accessing local static files if needed
    }

    try:
        wk_cmd = getattr(settings, 'WKHTMLTOPDF_CMD', None)
        config = pdfkit.configuration(wkhtmltopdf=wk_cmd) if wk_cmd else None
        pdf = pdfkit.from_string(html, False, options=options, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception:
        # Deliberately import here to keep pdfkit the primary dependency optional
        try:
            from xhtml2pdf import pisa
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            pisa.CreatePDF(html, dest=response)
            return response
        except Exception:
            # Final fallback: return simple HTML response indicating failure
            return HttpResponse('Unable to generate PDF at this time.', status=500)


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

    # Safely update existing report or create a new one (avoid IntegrityError)
    report, created = PredictionReport.objects.update_or_create(
        academic_record=record,
        defaults={
            'student': student,
            'risk_level': risk_level,
            # store as percentage 0-100 for template consistency
            'risk_score': round(score * 100.0, 3),
        }
    )

    return redirect('faculty_dashboard')