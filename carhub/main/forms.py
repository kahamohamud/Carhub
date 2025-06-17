from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Car

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_dealer', 'is_customer']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'model', 'year', 'price', 'image']
