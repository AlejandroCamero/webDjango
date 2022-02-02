from django.contrib import admin
from nucleo.models import User, Client, Employee, Category, Project, Participate
from django import forms
from django.contrib.auth.admin import UserAdmin

class EmployeeAdminForm(forms.ModelForm):
    def clean_dni(self):
        if len(self.cleaned_data['dni'])>9:
            raise forms.ValidationError('Dni no puede tener mas de 9 caracteres')
        elif len(self.cleaned_data['dni'])<9:
            raise forms.ValidationError('Dni no puede tener menos de 9 caracteres')
        else:
            return self.cleaned_data['dni']  

class EmployeeAdmin(admin.ModelAdmin):
    form=EmployeeAdminForm

class ClientAdminForm(forms.ModelForm):
    def clean_dni(self):
        if len(self.cleaned_data['dni'])>9:
            raise forms.ValidationError('Dni no puede tener mas de 9 caracteres')
        elif len(self.cleaned_data['dni'])<9:
            raise forms.ValidationError('Dni no puede tener menos de 9 caracteres')
        else:
            return self.cleaned_data['dni']  

class ClientAdmin(admin.ModelAdmin):
    form=ClientAdminForm
    
class ProjectAdminForm(forms.ModelForm):
    def clean_initDate(self):
        if self.cleaned_data['initDate']>self.cleaned_data['finDate']:
            raise forms.ValidationError('La fecha de inicio no puede ser mayor que la fecha final')
        else:
            return self.cleaned_data['initDate']
        
    def clean_finDate(self):
        if self.cleaned_data['finDate']<self.cleaned_data['initDate']:
            raise forms.ValidationError('La fecha final no puede ser menor que la fecha inicial')
        else:
            return self.cleaned_data['finDate'] 

class ProjectAdmin(admin.ModelAdmin):
    form=ProjectAdminForm
    
class ParticipateAdminForm(forms.ModelForm):
    def clean_role(self):
        if self.cleaned_data['role']!="ROLE_ADMIN" or self.cleaned_data['role']!="ROLE_CLIENTE" or self.cleaned_data['role']!="ROLE_ESPECIALISTA":
            raise forms.ValidationError('El rol debe ser ROLE_ADMIN, ROLE_CLIENTE o ROLE_ESPECIALISTA')
        else:
            return self.cleaned_data['role']

class ParticipateAdmin(admin.ModelAdmin):
    form=ParticipateAdminForm

# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Client)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Category)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Participate,ParticipateAdmin)