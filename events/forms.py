from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
        })
    )
    rsvp_deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
        })
    )

    class Meta:
        model = Event
        fields = [
            'name', 'description', 'date', 'venue',
            'contribution_amount', 'rsvp_deadline',
            'mpesa_paybill', 'mpesa_account', 'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'contribution_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'mpesa_paybill': forms.TextInput(attrs={'class': 'form-control'}),
            'mpesa_account': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }