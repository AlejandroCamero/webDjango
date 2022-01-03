from django.http.response import Http404
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView

# Create your views here.

def index(request):
    return redirect('index')