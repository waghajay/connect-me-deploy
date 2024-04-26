from django import forms
from django.contrib.auth.forms import PasswordResetForm , SetPasswordForm
from django.contrib.auth import password_validation


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email",'class' : 'form-control'}),
    )
    
class MyPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch":"The two password fields didn’t match.",
    }
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password" , "class" : "form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password" , "class" : "form-control"}),
    )