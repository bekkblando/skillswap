from django import forms
from django.contrib.auth.models import User
from swap.models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "* Username ↓"
        self.fields['password'].label = "* Password ↓"
        self.fields['email'].label = "* Email Address ↓"
        self.fields['username'].widget.attrs['placeholder'] = "Type Username Here"
        self.fields['password'].widget.attrs['placeholder'] = "Type Password Here"
        self.fields['email'].widget.attrs['placeholder'] = "Type Email Here"




    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['streetaddress'].label = "Street Address ↓"
        self.fields['city'].label = "City ↓"
        self.fields['zipcode'].label = "Zipcode ↓"
        self.fields['phone'].label = "Phone ↓"
        self.fields['age'].label = "Age ↓"

        self.fields['gender'].label = "Gender ↓"



        self.fields['gender'].widget.attrs['placeholder'] = "Gender Here"

        self.fields['age'].widget.attrs['age'] = "Enter Your Age Here"
        self.fields['streetaddress'].widget.attrs['placeholder'] = "Type Street Address Here"
        self.fields['city'].widget.attrs['placeholder'] = "Type City Name Here"
        self.fields['zipcode'].widget.attrs['placeholder'] = "Type Zipcode Here"
        self.fields['phone'].widget.attrs['placeholder'] = "Type Phone Number Here"

    class Meta:
        model = Profile
        fields = ['streetaddress','city','zipcode','state','phone',  'gender', 'age']


