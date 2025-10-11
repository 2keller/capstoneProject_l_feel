from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistration(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'bio']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'surname']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']
        