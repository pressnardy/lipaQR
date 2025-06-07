from django import forms
from . models import Order


class MenuForm(forms.Form):
    restaurant_id = forms.IntegerField()
    
    def __init__(self, *args, **kwargs):
        dynamic_fields = kwargs.pop('dynamic_fields', None)
        super().__init__(*args, **kwargs)
        if dynamic_fields:
            for field_name in dynamic_fields:
                self.fields[field_name] = forms.IntegerField(label='Quantity', min_value=0, required=False)
                
    items_ids = forms.JSONField()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['reference_number', 'phone_number', 'table_number', 'total_amount']
        widgets = {
            'reference_number': forms.TextInput(attrs={'disabled': True, 'name': 'reference_number'}),
            'total_amount': forms.NumberInput(attrs={'disabled': True, 'name': 'total_amount'}),
            'table_number': forms.NumberInput(attrs={'disabled': True, 'name': 'table_number'}),
            'phone_number': forms.TextInput(attrs={'required': True, 'name': 'phone_number'}),
        }
    
