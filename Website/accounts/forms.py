from django import forms
from .models import Profile
from django.contrib.auth.models import User

class UserSignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    firstname = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))
    password2 = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))

    def clean_username(self):
        user = self.cleaned_data['username']
        if User.objects.filter(username = user).exists():
            raise forms.ValidationError('User Exists')
        return user


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Exists')
        return email

    def clean_password2(self):
        password_1 = self.cleaned_data['password1']
        password_2 = self.cleaned_data['password2']
        if password_1 != password_2:
            raise forms.ValidationError('Passwords Do Not Match')
        elif len(password_2) <4:
            raise  forms.ValidationError('Password is Short')
        elif not any (x.isupper() for x in password_2):
            raise forms.ValidationError('Password Must Include at least One Capital letter')
        return password_2


class UserLoginForm(forms.Form):
    user = forms.CharField(max_length=50)
    password = forms.CharField(max_length=20)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =('phone','address','profile_image',)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model= User
        fields =('email','first_name','last_name')