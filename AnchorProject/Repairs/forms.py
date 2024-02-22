from django.forms import ModelForm
from django.forms import Form
from django import forms
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from .models import UserProfile, MechanicProfile


# Code added for loading form data on the Booking page
class UserRegisterForm(Form):
        type_user = (
                (1, 'Boat Owner'),
                (2, 'Mechanic')
        )
        username = forms.CharField(max_length= 100, label = "Write your name:")
        password = forms.CharField(max_length= 100, label = "Choose a password:", widget = forms.PasswordInput)
        phone_number = PhoneNumberField()
        type_of_user = forms.ChoiceField(choices = type_user, label = "How do you want to sign in?")
