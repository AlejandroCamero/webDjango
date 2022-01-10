from django import forms

from django.contrib.auth import get_user_model

from nucleo.models import Client
User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter username...','label':'Username'}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter email...','label':'Username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter first name...','label':'First name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter last name...','label':'Last name'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password...'})
        }
        
        def save(self):
            return User.objects.create_user(
                self.cleaned_data.get('username'),
                self.cleaned_data.get('email'),
                self.cleaned_data.get('password'),
            )
            
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields=['dni','name','surname','address','birthDate','idUser']
        widgets={
            'dni':forms.TextInput(attrs={'class':'form-control','placeholder':'DNI','label':'Username'}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre','label':'Username'}),
            'surname':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos','label':'First name'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Direccion','label':'Last name'}),
            'birthDate':forms.DateInput(attrs={'class':'form-control','placeholder':'Fecha de nacimiento','label':'Last name'}),
            'idUser':forms.NumberInput(attrs={'class':'form-control','placeholder':'Fecha de nacimiento','label':'Last name'}),
           
        }
        
        def save(self):
            return Client.objects.create_user(
                self.cleaned_data.get('dni'),
                self.cleaned_data.get('name'),
                self.cleaned_data.get('surname'),
                self.cleaned_data.get('address'),
                self.cleaned_data.get('birthDate'),
                self.cleaned_data.get('idUser')
            )