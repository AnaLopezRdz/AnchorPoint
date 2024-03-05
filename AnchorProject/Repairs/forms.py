from django.forms import Form
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.forms.widgets import TextInput
from django.utils.html import format_html


class TelInput(TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        tel_html = super().render(name, value, attrs, renderer)
        return format_html('<div class="tel-input" style="display: flex;">{}</div>', tel_html)


class UserRegisterForm(Form):
    type_user = (
            (1, 'Boat Owner'),
            (2, 'Mechanic')
    )
    username = forms.CharField(max_length=100, label="Write your name:")
    password = forms.CharField(max_length=100, label="Choose a password:", widget=forms.PasswordInput)
    phone = PhoneNumberField(widget=TelInput())
    type_of_user = forms.ChoiceField(choices=type_user, label="How do you want to sign in?")

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.fields['type_of_user'].widget.attrs['class'] = 'form-select'

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['username'].help_text = "<span class='form-text text-muted'></span>"

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'password'
        self.fields['password'].help_text = "<span class='form-text text-muted'></span>"

        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['type'] = 'tel'
