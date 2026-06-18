from django import forms
import re

class AdminRegisterForm(forms.Form):

    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):

        password = self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError(
                "Password must contain at least 8 characters."
            )

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r'[a-z]', password):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r'\d', password):
            raise forms.ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(r'[@$!%*?&]', password):
            raise forms.ValidationError(
                "Password must contain at least one special character."
            )

        return password


class AdminLoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())