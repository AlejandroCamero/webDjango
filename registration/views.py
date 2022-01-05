from django import forms
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from nucleo.models import User, Client
import datetime

from registration.forms import UserCreationFormWithEmail, ClientForm

# Create your views here.

class ClientCreate(CreateView):
    form_class = ClientForm
    second_form_class = UserCreationFormWithEmail
    template_name = 'registration/register.html'
    
    def get_success_url(self):
        return reverse_lazy('login')+'/?register'
    
    def get_context_data(self, **kwargs):
        context = super(ClientCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            client = form.save(commit=False)
            client.idUser = form2.save()
            client.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
    
    # def get_context_data(self, **kwargs):
    #     # we need to overwrite get_context_data
    #     # to make sure that our formset is rendered
    #     data = super(ClientCreate, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         data["user"] = UserCreationFormWithEmail(self.request.POST)
    #     else:
    #         data["user"] = UserCreationFormWithEmail()
    #     return data
    
    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     user = context["user"]
    #     self.object = form.save()
    #     if user.is_valid():
    #         user.instance = self.object
    #         user.save()
    #     return super().form_valid(form)
    