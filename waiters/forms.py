from django import forms
from menus.models import Order, Waiter

class CreateWaiterForm(forms.ModelForm):
    class Meta:
        model = Waiter
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'id': 'waiter-name', 'class': 'form-input', 'required':'required'}),
            'phone_number': forms.TextInput(attrs={'id': 'phone_number', 'class': 'form-input', 'required': 'required'}),
            'national_id': forms.NumberInput(attrs={'id': 'national-id', 'class': 'form-input', 'required': 'required'}),
            'pin': forms.NumberInput(attrs={'id': 'pin', 'class': 'form-input', 'required': 'required'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['reference_number', 'table_number',]
        widgets = {
            'reference_number': forms.TextInput(attrs={'disabled': True, 'name': 'reference_number'}),
            # 'total_amount': forms.NumberInput(attrs={'disabled': True, 'name': 'total_amount'}),
            'table_number': forms.NumberInput(attrs={'disabled': True, 'name': 'table_number'}),
            # 'phone_number': forms.TextInput(attrs={'required': True, 'name': 'phone_number'}),
        }

    

