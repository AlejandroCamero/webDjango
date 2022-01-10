from django.http.response import  HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.views.generic.detail import DetailView
from nucleo.models import User, Client
from django.utils.decorators import method_decorator


from registration.forms import UserCreationFormWithEmail, ClientForm
from registration.decorators import same_user, same_client
# Create your views here.

@method_decorator(same_user, name='dispatch')
class ClientDetailsView(DetailView):
    model = User
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['client'] = Client.objects.get(idUser=self.request.user)
        return context
    

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

@method_decorator(same_client, name='dispatch')       
class ClientUpdate(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'registration/register.html'
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def get_context_data(self, **kwargs):
        context = super(ClientUpdate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context

@method_decorator(same_user, name='dispatch')
class UserUpdate(UpdateView):
    model = User
    form_class = UserCreationFormWithEmail
    template_name = 'registration/register.html'
    
    def get_success_url(self):
        return reverse_lazy('index')
    
    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context
    
    