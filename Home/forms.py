from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError
import re

# Creating Forms for create user...
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email","password1", "password2"]

class UpdateUserForm(forms.ModelForm):
    password = forms.CharField(
        label='New Password (optional)', 
        max_length=128, 
        required=False, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password', 'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password', 
        max_length=128, 
        required=False, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Exclude password here
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'form-control'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 8 or not re.search(r'\d', password) and not re.search(r'\W', password):
                raise ValidationError("Password must be at least 8 characters long and contain at least one digit or special character.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data
    

class SendFile(forms.Form):
    File = forms.FileField(
        label='Upload File', 
        required=True, 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    Notes = forms.CharField(
        label='Notes', 
        max_length=254, 
        required=False, 
        widget=forms.Textarea(attrs={'placeholder': 'Enter your message here...', 'class': 'form-control'})
    )
    Email = forms.EmailField(
        label='Email', 
        max_length=254,  
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Your Key', 'class': 'form-control'})
    )

    
