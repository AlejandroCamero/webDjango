from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime
from django.db.models.fields import TextField
from django.forms.fields import CharField
from django.forms.widgets import Textarea

from .models import Project, Category

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
    initialDate = datetime.datetime.now().strftime('%Y-%m-%d')
    
    
    title = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Título del proyecto'}), label='Título')
    description = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Descripción del proyecto'}), label='Descripción')
    level = forms.IntegerField(widget= forms.NumberInput(attrs={'class': 'form-control mb2', 'placeholder': 'Nivel del proyecto', 'min':0, 'max':10}), label='Nivel')
    initDate = forms.DateField(widget= forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control','type':'date', 'min': initialDate}), label='Fecha de inicio')
    finDate = forms.DateField(widget= forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control','type':'date', 'min': initialDate}), label='Fecha de fin')
    report = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Informe'}), label='Informe del pryecto')
    idCategory = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control mb2', 'placeholder': 'Categoría'}), label='Categoría')
    
    class Meta:
        model=Project
        fields=['title','description','level','initDate', 'finDate', 'report', 'idCategory']
    
class ProjectFormUpdate(forms.ModelForm):
    initialDate = datetime.datetime.now().strftime('%Y-%m-%d')
    
    
    title = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Título del proyecto'}), label='Título')
    description = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Descripción del proyecto'}), label='Descripción')
    level = forms.IntegerField(widget= forms.NumberInput(attrs={'class': 'form-control mb2', 'placeholder': 'Nivel del proyecto', 'min':0, 'max':10}), label='Nivel')
    finDate = forms.DateField(widget= forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control','type':'date', 'min': initialDate}), label='Fecha de fin')
    report = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Informe'}), label='Informe del pryecto')
    idCategory = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control mb2', 'placeholder': 'Categoría'}), label='Categoría')
    
    class Meta:
        model=Project
        fields=['title','description','level', 'finDate', 'report', 'idCategory']