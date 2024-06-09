from django import forms
from django.contrib.auth.models import User

class userSignupForm(forms.ModelForm):
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_password(self):
        """Check if the password length is at least 4 long"""
        cd = self.cleaned_data
        if cd['password'] and len(cd['password']) < 4:
            raise forms.ValidationError('Password must be at least 4 characters long.')
        return cd['password']

    def clean_password2(self):
        """Check if the password fields match."""
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password2') and cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_new_password2(self):
        cd = self.cleaned_data
        if cd.get('new_password') and cd.get('new_password2') and cd['new_password'] != cd['new_password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['new_password2']