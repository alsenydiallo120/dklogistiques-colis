from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView
from accounts.forms import RegisterEditForm, RegisterForm
from django.contrib import messages
from accounts.models import CustomUser
from accounts.forms import *
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import View



class Logout(View):
   def get(self, request, *args, **kwargs):
        logout(request) 
        return redirect(reverse_lazy("login"))
      


class reset_password(UpdateView):
    model = CustomUser
    form_class=updatePasswordForm
    template_name = "registration/reset_password.html"
    success_url = reverse_lazy('accounts-listes')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            messages.success(self.request, "Modification éffectuée avec succès")
        return super().form_valid(form)



def page_not_found(request,exception):
    return render(request,'error_404.html')


class register(CreateView):
    models = CustomUser
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('accounts-register')

    def form_valid(self, form):
        messages.success(self.request, "Utilisateur ajouté avec succès")
        return super().form_valid(form)

class liste(ListView):
    model = CustomUser
    template_name = "registration/listedesutilisateurs.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = CustomUser.objects.all()
        return context
    

class edit(UpdateView):
    model = CustomUser
    template_name = "registration/edit.html"
    form_class = RegisterEditForm
    success_url = reverse_lazy('accounts-listes')
    def form_valid(self, form):
        messages.success(self.request, "Utilisateur ajouté avec succès")
        return super().form_valid(form)

def login_client(request):
    form = ConnexionForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/accounts/profile/')
    return render(request, "registration/loginclient.html",{'form':form})