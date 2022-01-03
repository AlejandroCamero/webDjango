from django.contrib import admin
from nucleo.models import User, Client, Employee, Category, Project, Participate

from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Participate)