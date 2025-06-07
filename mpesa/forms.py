from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['reference_number', 'total_amount', 'phone_number']
        widgets = {
            'reference_number': forms.TextInput(attrs={'disabled': True, 'name': 'reference_number'}),
            'total_amount': forms.NumberInput(attrs={'disabled': True, 'name': 'total_amount'}),
            'phone_number': forms.TextInput(attrs={'required': True, 'name': 'phone_number'}),
        }


