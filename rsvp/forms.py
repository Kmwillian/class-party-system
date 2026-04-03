from django import forms
from .models import RSVPEntry


class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVPEntry
        fields = ['full_name', 'registration_number', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. John Kamau',
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. SCT221-0001/2021',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g. 0712345678',
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'registration_number': 'Registration Number',
            'phone_number': 'Phone Number (for M-Pesa)',
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        phone = phone.replace(' ', '').replace('-', '')
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif phone.startswith('+'):
            phone = phone[1:]
        if not phone.startswith('254') or len(phone) != 12:
            raise forms.ValidationError('Enter a valid Kenyan phone number e.g. 0712345678')
        return phone

    def clean_registration_number(self):
        reg = self.cleaned_data.get('registration_number', '').strip().upper()
        return reg