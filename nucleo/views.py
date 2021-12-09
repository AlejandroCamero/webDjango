from django.http.response import Http404
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        print(username)
        print(password)
        if user:
            login(request,user)
            messages.success(request,"Welcome {}! ".format(user.username))
            return redirect('index')
        else:
            messages.error(request,"Username or password incorrect")
        
    
    return render(request,'index.html',{
        
    })
    
def users(request):
    users=User.objects.all()
    return render(request,"users.html",{'users':users})

def usersDetails(request,user_id):
    try:
        user=User.objects.get(pk=user_id)
    except:
        raise Http404('No existe')
    context={'user':user}
    return render(request,"userDetails.html",{'user':user})