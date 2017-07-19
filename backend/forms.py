from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    remember = forms.BooleanField(False)
    captcha = CaptchaField()
