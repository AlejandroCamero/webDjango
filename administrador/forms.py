from django import forms
from nucleo.models import User, Client, Employee

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('dni', 'name', 'surname', 'address', 'birthDate')
        widgets = {
            'dni' : forms.TextInput(attrs={'class' : 'form-control mb2', 'placeholder' : 'DNI del Cliente'}),
            'name' : forms.TextInput(attrs={'class' : 'form-control mb2', 'placeholder' : 'Nombre'}),
            'surname' : forms.TextInput(attrs={'class' : 'form-control mb2', 'placeholder' : 'Apellidos'}),
            'address' : forms.TextInput(attrs={'class' : 'form-control mb2', 'placeholder' : 'Dirección'}),
            'birthDate' : forms.DateInput(format=('%Y-%m-%d'), attrs={'class' : 'form-control mb2', 'type' : 'date', 'placeholder' : 'Fecha de nacimiento'}),
        }
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('dni', 'name', 'surname', 'address', 'biography')
        widgets = {
            'dni' : forms.TextInput(attrs={'class' : 'form-control mb2', 'placeholder' : 'DNI del Empleado'}),
            'name' : forms.TextInput(attrs={'class' : 'form-control mb2', 'placeholder' : 'Nombre'}),
            'surname' : forms.TextInput(attrs={'class' : 'form-control mb2', 'placeholder' : 'Apellidos'}),
            'address' : forms.TextInput(attrs={'class' : 'form-control mb2', 'placeholder' : 'Dirección'}),
            'biography' : forms.TextInput(attrs={'class' : 'form-control mb2', 'placeholder' : 'Biografía'}),
        }