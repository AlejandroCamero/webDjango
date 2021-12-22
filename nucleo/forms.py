from django import forms

from django.contrib.auth.models import User
from django.db.models.fields import TextField
from django.forms.fields import CharField
from django.forms.widgets import Textarea

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter username...'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password...'})
        }
        
    # username=forms.CharField(label="Username",required=True,widget=forms.TextInput(
    #     attrs={'class':'form-control','placeholder':'Enter username...'}
    #     ))
    # password=forms.CharField(label="Password",required=True,widget=forms.PasswordInput(
    #     attrs={'class':'form-control','placeholder':'Enter password...'}
    #     ))