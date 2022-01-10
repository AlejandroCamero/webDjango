from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import UserForm,ClientForm

from nucleo.models import Client

User = get_user_model()
# Create your views here.

def register(request):
    form=ClientForm(request.POST or None)
    userform=UserForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        
        cliente = form.save()
        user = userform.save()
                
        if user:
            login(request,user)
            messages.success(request,'User created succesfully')
            return redirect('/')
        
    return render(request,'nucleo/user_form.html',{
        'form':form,
        'form2':userform
    })