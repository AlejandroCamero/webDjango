from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import messages

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username
    
    def getFullName(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
    @receiver(user_logged_out)
    def on_user_logged_out(sender, request, **kwargs):
        user = request.user.username
        messages.add_message(request, messages.INFO, 'El usuario {} ha salido del sistema'.format(user))
    
class Employee(models.Model):
    dni = models.CharField(max_length=9, verbose_name="DNI")
    name = models.CharField(max_length=40, verbose_name="Nombre")
    surname = models.CharField(max_length=60, verbose_name="Apellidos")
    address = models.CharField(max_length=150, verbose_name="Direccion")
    biography = models.CharField(max_length=255, verbose_name="Biografía")
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    
    def __str__(self):
        return self.name + " " + self.surname
    
class Client(models.Model):
    dni = models.CharField(max_length=9, verbose_name="DNI")
    name = models.CharField(max_length=40, verbose_name="Nombre")
    surname = models.CharField(max_length=60, verbose_name="Apellidos")
    address = models.CharField(max_length=150, verbose_name="Dirección")
    birthDate = models.DateField(verbose_name="Fecha de nacimiento")
    dischargeDate = models.DateField(verbose_name="Fecha de alta", default = datetime.date.today())
    active = models.IntegerField(verbose_name="Activo", default=0)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    
    def __str__(self):
        return self.name + " " + self.surname

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    photo = models.CharField(max_length=255, verbose_name="Foto")
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=150, verbose_name="Título")
    description = models.CharField(max_length=255, verbose_name="Descripción")
    level = models.IntegerField(verbose_name="Nivel")
    initDate = models.DateField(verbose_name="Fecha de inicio")
    finDate = models.DateField(verbose_name="Fecha de finalización")
    report = models.CharField(max_length=255, verbose_name="Informe final")
    idEmployee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Empleado")
    idCategory = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoría")
    
    def __str__(self):
        return self.title
    

class Participate(models.Model):
    idClient = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    idProject = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Proyecto")
    enrollmentDate = models.DateField(verbose_name="Fecha de inscripción")
    role = models.CharField(max_length=100, verbose_name="Rol")
    

