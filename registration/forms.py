from django import forms
from django.contrib.auth.forms import UserCreationForm
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
            'biography' : forms.Textarea(attrs={'class' : 'form-control mb2', 'placeholder' : 'Biografía', 'rows' : 3}),
        }        

class UserCreationFormWithEmail(UserCreationForm):
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control mb2', 'placeholder': 'Username'}), label='Nombre de usuario')
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb2', 'placeholder': 'Email'}), max_length=254, help_text='Introduce una dirección de email válida.')
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb2', 'placeholder': 'Contraseña'}), label="Contraseña")
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb2', 'placeholder': 'Repite contraseña'}), label="Repite Contraseña")
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
        
        def save(self, commit=True):
            user = super(UserCreationFormWithEmail, self).save()
            user.email = self.clean_email()
            user.save()
            
            return user
        
        def clean(self):
            value = self.cleaned_data.get('email')
            if User.objects.filter(email=value).exists():
                raise forms.ValidationError('Email ya registrado, prueba otro.')
            return self.cleaned_data
