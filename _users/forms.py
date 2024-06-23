from django import forms
from django.forms import widgets, Widget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django_countries.widgets import CountrySelectWidget




class onboardForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country']
        #widgets = {"country": CountrySelectWidget('{widget}')}

class UserSignInForm(forms.Form):
    username = forms.CharField(label="Enter username or Email",max_length=100, required=True)
    password = forms.CharField(label="Enter Password",widget=forms.PasswordInput())

    # class Meta:
        # models = AuthenticationForm
        # fields = ['username', 'password']

        

    # def __init__(self, *args, **kwargs):
    #     super(UserSignInForm, self).__init__(*args, **kwargs)

    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'id':"hi"})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username']
        labels = {
             "first_name":"Name"
        }


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        placeholderDict = {
             "first_name":"Enter your name",
             "email":"Enter your name",
             "username":"Enter your username",
             "password1":"Enter your password",
             "password2":"Enter your password again",
        }

        for name, field in self.fields.items():
                field.widget.attrs.update({'required':'', 'placeholder':placeholderDict[name]})
        
        self.fields['username'].widget.attrs.update({'autofocus':False})
        self.fields['username'].help_text = "Can contain (A-Z, a-z, 0-9, @, ., +, -, _) max. 150 Chars"









    

    

    