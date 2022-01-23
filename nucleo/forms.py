from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.fields import TextField
from django.forms.fields import CharField
from django.forms.widgets import Textarea

from .models import Project

User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter username...'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password...'})
        }
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=['title','description','level','initDate','report']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter title...'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter description...'}),
            'level':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter level...'}),
            'initDate':forms.DateInput(attrs={'class':'form-control','placeholder':'Enter description...'}),
            'report':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter report...'})
        }
        
    # username=forms.CharField(label="Username",required=True,widget=forms.TextInput(
    #     attrs={'class':'form-control','placeholder':'Enter username...'}
    #     ))
    # password=forms.CharField(label="Password",required=True,widget=forms.PasswordInput(
    #     attrs={'class':'form-control','placeholder':'Enter password...'}
    #     ))