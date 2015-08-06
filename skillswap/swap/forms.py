from django import forms
from django.contrib.auth.models import User
from swap.models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "* Username:"
        self.fields['password'].label = "* Password:"
        self.fields['email'].label = "* Email Address:"


    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['streetaddress','city','zipcode','state','phone']
