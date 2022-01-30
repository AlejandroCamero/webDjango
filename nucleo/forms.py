from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime

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
    report = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Informe'}), label='Informe del proyecto')
    idCategory = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control mb2', 'placeholder': 'Categoría'}), label='Categoría')
    
    class Meta:
        model=Project
        fields=['title','description','level','initDate', 'finDate', 'report', 'idCategory']
        
    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        errors = []
        
        if 'initDate' in cleaned_data.keys() and 'finDate' in cleaned_data.keys():
            begin_date = cleaned_data['initDate']
            final_date = cleaned_data['finDate']
            if begin_date < datetime.datetime.now().date():
                begin_date = None
                errors.append(forms.ValidationError("La fecha de inicio no puede ser inferior al día actual."))
            elif final_date < begin_date:
                begin_date = None
                final_date = None
                errors.append(forms.ValidationError("La fecha de fin no puede ser menor a la de inicio."))
            
            if errors:
                raise forms.ValidationError(errors)

        return cleaned_data
    
class ProjectFormUpdate(forms.ModelForm):
    initialDate = datetime.datetime.now().strftime('%Y-%m-%d')
    
    
    title = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Título del proyecto'}), label='Título')
    description = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Descripción del proyecto'}), label='Descripción')
    level = forms.IntegerField(widget= forms.NumberInput(attrs={'class': 'form-control mb2', 'placeholder': 'Nivel del proyecto', 'min':0, 'max':10}), label='Nivel')
    finDate = forms.DateField(widget= forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control','type':'date', 'min': initialDate}), label='Fecha de fin')
    report = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Informe'}), label='Informe del proyecto')
    idCategory = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control mb2', 'placeholder': 'Categoría'}), label='Categoría')
    
    class Meta:
        model=Project
        fields=['title','description','level', 'finDate', 'report', 'idCategory']
        
    def clean(self):
        cleaned_data = super(ProjectFormUpdate, self).clean()
        errors = []
        instance = self.instance
        
        if 'finDate' in cleaned_data.keys() and instance is not None and instance.id is not None:
            final_date = cleaned_data['finDate']
            if final_date < instance.initDate:
                final_date = None
                errors.append(forms.ValidationError("La fecha de fin no puede ser menor a la de inicio."))
            
            if errors:
                raise forms.ValidationError(errors)

        return cleaned_data