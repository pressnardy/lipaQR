from menus.models import Order, Item
from django import forms

class AddItemForm(forms.ModelForm):
    AVAILABLE_CHOICES = [
        ('available', 'Available')
    ]
    class meta:
        model = Item
        fields = ['name', 'unit', 'unit_price', 'image', 'description', 'available']
    available = forms.ChoiceField(choices=AVAILABLE_CHOICES, widget=forms.Select(
            attrs={'name': 'available', 'id':'available', 'class': 'form-input'}
        ))


    def save(self, *args, **kwargs):
        self.available = self.available == 'available'
        super().save(*args, **kwargs)
    