from django.contrib import admin
from nucleo.models import User, Client, Employee, Category, Project, Participate

# Register your models here.
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Participate)