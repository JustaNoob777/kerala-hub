# forms.py
from django import forms

class SimpleLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Email",
            "autocomplete": "email",
            "required": True,
            "class": "input-email"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "autocomplete": "current-password",
            "required": True,
            "class": "input-password"
        })
    )