# academics/forms.py
from django import forms
from .models import AcademicRecord

class AcademicRecordForm(forms.ModelForm):
    class Meta:
        model = AcademicRecord
        fields = ['semester', 'attendance_percentage', 'sgpa', 'cgpa', 'backlogs_current', 'fee_dues']
        
        # We replace "form-control" with Tailwind utility classes
        widgets = {
            'semester': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-zinc-200 focus:ring-2 focus:ring-brand-500 outline-none transition-all'}),
            'attendance_percentage': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-zinc-200 focus:ring-2 focus:ring-brand-500 outline-none transition-all'}),
            'sgpa': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-zinc-200 focus:ring-2 focus:ring-brand-500 outline-none transition-all', 'step': '0.01'}),
            'cgpa': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-zinc-200 focus:ring-2 focus:ring-brand-500 outline-none transition-all', 'step': '0.01'}),
            'backlogs_current': forms.NumberInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-zinc-200 focus:ring-2 focus:ring-brand-500 outline-none transition-all'}),
            'fee_dues': forms.CheckboxInput(attrs={'class': 'w-5 h-5 rounded border-zinc-300 text-brand-600 focus:ring-brand-500'}),
        }