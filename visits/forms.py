from django import forms
from .models import Visit, MedicalReport, Availability


class VisitRequestForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = ['file']


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['day', 'time_slot']
