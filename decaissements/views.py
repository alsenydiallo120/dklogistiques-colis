from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from CGEI.my_functions import *
from .models import Decaissement
from .forms import *
from colis.models import *
from depenses.models import *





def view_decaissements(request):
    context={}
    if request.user.agences.pays.libelle=="France":
        context['caisse_euro']= caisse_paris(request.user.id)
        context['pays']= "France"
    else:
        context["caisse_gnf"]=caisse_guinee(request.user.id,"gnf")
        context["caisse_euro"]=caisse_guinee(request.user.id,"€")
        context['pays']= "Guinee"
    context["etat"]=1
    return render(request,"decaissements/view_decaissements.html",context)



class valide_encaissement(UpdateView):
    model = Decaissement
    form_class = ValideForm
    template_name = 'decaissements/valider.html'
    success_url = reverse_lazy('encaissement_valide')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj=self.get_object()
        context["obj"] =obj 
        return context

    def form_valid(self, form):
        form.instance.etat=True
        form.instance.validate_by_id=self.request.user.id
        return super().form_valid(form)
    



class create(CreateView):
    model = Decaissement
    form_class = DecaissementForm
    template_name = 'decaissements/create.html'
    success_url = reverse_lazy('decaissements-index')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        return initial

    def form_valid(self, form):
        form.instance.emetteur_id=self.request.user.id
        form.instance.agences_id=self.request.user.agences_id
        return super().form_valid(form)
    

class encaissement_enattente(ListView):
    model = Decaissement
    template_name = 'decaissements/index.html'
    context_object_name = 'decaissements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"]="Liste des encaissements en attente de validation"
        if self.request.user.is_superuser or self.request.user.username == "traore":
            context["decaissements"] = Decaissement.objects.filter(etat=False,recepteur=self.request.user.id)
        else:
            context["decaissements"] = Decaissement.objects.filter(etat=False,emetteur=self.request.user.id)
        return context



class encaissement_valide(ListView):
    model = Decaissement
    template_name = 'decaissements/index.html'
    context_object_name = 'decaissements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"]="Liste des encaissements validés"
        if self.request.user.is_superuser or self.request.user.username == "traore":
            if self.request.user.is_superuser:
                context["decaissements"] = Decaissement.objects.filter(etat=True)
            else:
                context["decaissements"] = Decaissement.objects.filter(etat=True,recepteur_id=self.request.user.id)
        else:
            context["decaissements"] = Decaissement.objects.filter(etat=True,emetteur=self.request.user.id)
        return context
    


class index(ListView):
    model = Decaissement
    template_name = 'decaissements/index.html'
    context_object_name = 'decaissements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"]="Liste des encaissements"
        context["decaissements"] = Decaissement.objects.filter(emetteur=self.request.user.id)
        return context
    


class edit(UpdateView):
    model = Decaissement
    form_class = DecaissementForm
    template_name = 'decaissements/edit.html'
    success_url = reverse_lazy('decaissements-index')


    
class delete(DeleteView):
    model = Decaissement
    template_name = 'decaissements/edit.html'
    success_url = reverse_lazy('decaissements-index')
    success_message = 'Suprression effectuee avec succes'

