from django import forms
from .models import Encounter
from .models import Member, Patient

class EncounterForm(forms.ModelForm):
    class Meta:
        model = Encounter
        fields = [
            'enc_patient_query', 'enc_physician_finding', 'enc_prescription', 'enc_lab_test',
            'enc_diet', 'enc_allergy', 'enc_remark', 'enc_time_start', 'enc_time_end'
        ]
        widgets = {
            'enc_time_start': forms.TimeInput(attrs={'id': 'starttime','type': 'time'}),
            'enc_time_end': forms.TimeInput(attrs={'id':'endtime','type': 'time'}),
            'enc_patient_query': forms.Textarea(attrs={'id':'patient_query','rows': 3}),
            'enc_physician_finding': forms.Textarea(attrs={'id':'physician_finding','rows': 4}),
            'enc_prescription': forms.Textarea(attrs={'id':'prescription','rows': 4}),
            'enc_lab_test': forms.Textarea(attrs={'id':'lab_test','rows': 4}),
            'enc_diet': forms.Textarea(attrs={'id':'diet','rows': 3}),
            'enc_allergy': forms.Textarea(attrs={'id':'allergy','rows': 3}),
            'enc_remark': forms.Textarea(attrs={'id':'remark','rows': 3}),
        }
class EncounterFilterForm(forms.Form):
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    physician = forms.ModelChoiceField(queryset=Member.objects.all(), required=False, empty_label="All Physicians")
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=False, empty_label="All Patients")
