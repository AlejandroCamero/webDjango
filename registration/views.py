from django.shortcuts import render

from django.views.generic.edit import CreateView,DeleteView,UpdateView

from django.contrib.auth.models import User

from .forms import UserForm

# Create your views here.

class UserCreate(CreateView):
    form_class=UserForm
    model = User
    success_url="usersView"
    
class UserDelete(DeleteView):
    model=User
    success_url="../usersView"