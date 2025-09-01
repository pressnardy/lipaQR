from django import forms
from menus.models import Item, Restaurant
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User


class AddRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'email', 'phone_number', 'till_number']
        widgets = {
            'name': forms.TextInput(attrs={'name': 'name', 'id': 'name', 'class': 'form-input', 'placeholder':'restaurant name', 'required': True}),
            'location': forms.TextInput(attrs={'name': 'location', 'id': 'location', 'class': 'form-input', 'placeholder':'location', 'required': True}),
            'email': forms.EmailInput(attrs={'name': 'email', 'id': 'email', 'class': 'form-input', 'placeholder':'email', 'required': True}),
            'phone_number': forms.TextInput(attrs={'name': 'phone_number', 'id': 'phone-number', 'class': 'form-input', 'placeholder':'phone number', 'required': True}),
            'till_number': forms.NumberInput(attrs={'name': 'till_number', 'id': 'till-number', 'class': 'form-input', 'placeholder':'till number', 'required': True})
        }

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'unit', 'description', 'available', 'unit_price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'name': 'name', 'id': 'name', 'class': 'form-input', 'placeholder': 'Item Name'}),
            'unit': forms.TextInput(attrs={'name': 'unit', 'id': 'unit', 'class': 'form-input', 'placeholder': 'Unit'}),
            'description': forms.Textarea(attrs={'name': 'description', 'id': 'description', 'class': 'form-input', 'placeholder': 'Description'}),
            'unit_price': forms.NumberInput(attrs={'name': 'unit_price', 'id': 'unit_price', 'class': 'form-input', 'placeholder': 'Unit Price'}),
            'image': forms.ClearableFileInput(attrs={'name': 'image', 'id': 'image'}),
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'unit', 'description', 'available', 'category', 'unit_price']
        widgets = {
            'name': forms.TextInput(attrs={'name': 'name', 'id': 'name', 'class': 'form-input', 'placeholder': 'Item Name'}),
            'description': forms.Textarea(attrs={'name': 'description', 'id': 'description', 'class': 'form-input', 'placeholder': 'Description'}),
            'unit': forms.TextInput(attrs={'name': 'unit', 'id': 'unit', 'class': 'form-input', 'placeholder': 'Unit'}),
            'unit_price': forms.NumberInput(attrs={'name': 'unit_price', 'id': 'unit_price', 'class': 'form-input', 'placeholder': 'Unit Price'}),
            'available': forms.Select(
                choices=[('available', 'Available'), ('unavailable', 'Unavailable')],
                attrs={'name': 'available', 'id': 'available', 'class': 'form-input'}
            ),
            'category': forms.Select(
                choices=[('drinks', 'Drinks'), ('beverages', 'Beverages'), ('snarks', 'Snarks'), ('meat', 'Meat'), ('other', 'Other')],
                attrs={'name': 'available', 'id': 'available', 'class': 'form-input'}
            ),
        }
        
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name',]
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Email', 'required': True, 'name': 'username', 'id': 'email'}),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Password', 'required': True, 'id': 'password', 'name': 'password1'}),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm Password', 'required': True, 'id': 'password2', 'name': 'password2'}),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Phone Number', 'required': True, 'name': 'first_name', 'id': 'phone-number'}),
        }


class LoginForm:
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Email', 'required': True, 'name': 'email', 'id': 'email'
    })),
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password', 'required': True, 'id': 'password', 'name': 'password'
    }))

