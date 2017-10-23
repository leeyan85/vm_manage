#-*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput
class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="domain username",
        error_messages={'required': 'please input the username'},
        widget=forms.TextInput(
            attrs={
                'placeholder':"username",
                'class':"form-control span12"
            }
        ),
    )    
    password = forms.CharField(
        required=True,
        label="domain password",
        error_messages={'required': 'please input password'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':"password",
                'class':"form-controlspan12 form-control"
            }
        ),
    )  
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("user name and password are required")
        else:
            cleaned_data = super(LoginForm, self).clean()

class RegularForm(forms.Form):
    
    ipaddr = forms.CharField(
            required=True,
            label="IP Address",
            error_messages={'required': 'please input the ipaddress'},
            widget=forms.TextInput(
                attrs={
                    'placeholder':"",
                    'class':"form-control span12",
                    'value': ''           
                }
            ),
    )    
    vmpasswd= forms.CharField(
            required=True,
            label="new password",
            error_messages={'required': 'please input password'},
            widget=forms.PasswordInput(
                attrs={
                    'placeholder':"",
                    'class':"form-controlspan12 form-control"
                }
            ),
        )  
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("IP and password are required")
        else:
            cleaned_data = super(RegularForm, self).clean()

            