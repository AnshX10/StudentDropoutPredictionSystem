# counseling/forms.py
from django import forms
from .models import CounselingSession

class CounselingSessionForm(forms.ModelForm):
    class Meta:
        model = CounselingSession
        fields = ['session_date', 'notes', 'progress_status']
        
        widgets = {
            'session_date': forms.DateInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-zinc-200 focus:ring-2 focus:ring-brand-500 outline-none transition-all', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-zinc-200 focus:ring-2 focus:ring-brand-500 outline-none transition-all', 'rows': 4}),
            'progress_status': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-zinc-200 focus:ring-2 focus:ring-brand-500 outline-none transition-all'}),
        }