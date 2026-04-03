from django import forms
from .models import Payment


class MarkCashPaidForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['reference_code']
        widgets = {
            'reference_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional receipt or reference',
            })
        }
        labels = {
            'reference_code': 'Reference / Receipt (optional)',
        }