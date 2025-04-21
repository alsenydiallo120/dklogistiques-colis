from django.views.generic import CreateView, ListView, DeleteView, UpdateView,DetailView
from django.urls import reverse_lazy
from colis.models import Coli
from .models import Embarquement,CodeEmbarquement,DetailEmbarquement
from .forms import *
from lots.models import Lot,DetailLot
from django.db import transaction
from querystring_parser import parser
from datetime import date,datetime
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect




class delete(DeleteView):
    model = Embarquement
    template_name = 'embarquements/edit.html'
    success_url = reverse_lazy('embarquements-index')
    success_message = 'Suprression effectuee avec succes'
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        lots=DetailEmbarquement.objects.filter(embarquements_id=self.kwargs['pk'])
        for l in lots:
            colis=DetailLot.objects.filter(lots_id=l.lots_id)
            lot=Lot.objects.get(id=l.lots_id)
            lot.etat_embarqment=0
            lot.save()
            for c in colis:
                coli=Coli.objects.get(id=c.colis_id)
                coli.etat_embarquement=0
                coli.date_embarquement=None
                coli.heure_embarquement=None
                coli.save()
        return self.delete(request, *args, **kwargs)

    # def form_valid(self, form):
    #     lots=DetailEmbarquement.objects.filter(id=self.kwargs['pk'])
    #     print("LOTS",lots)
    #     return HttpResponse()
        # datejour = date.today()
        # heurejour = datetime.now()
        # for l in lots:
        #     colis=DetailLot.objects.filter(lots_id=l)
        #     for c in colis:
        #         coli=Coli.objects.get(id=c.colis_id)
        #         coli.etat_embarquement=1
        #         coli.date_embarquement=datejour
        #         coli.heure_embarquement=heurejour
        #         coli.save()
        # self.object.delete()
        # return HttpResponseRedirect(self.get_success_url())



class create(CreateView):
    model = Embarquement
    form_class = EmbarquementForm
    template_name = 'embarquements/create.html'
    success_url = reverse_lazy('embarquements-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lots"] = Lot.objects.filter(agences_id=self.request.user.agences.id,etat_embarqment=0)
        if self.request.user.is_superuser:
            coldembarquement="LDKLV"+str(self.request.user.id)+"-"+"ADM"+str(CodeEmbarquement.objects.count())
        else:
            coldembarquement="LDKLV"+str(self.request.user.id)+"-"+str(self.request.user.agences.pays.libelle)[0:1]+str(CodeEmbarquement.objects.count())
        context["codembarquement"] = coldembarquement 
        context["transporform"] = EmbarquementForm() 
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        lots = parser.parse(self.request.POST.urlencode())['lots']
        datejour = date.today()
        heurejour = datetime.now()
        for l in lots:
            colis=DetailLot.objects.filter(lots_id=l)
            for c in colis:
                coli=Coli.objects.get(id=c.colis_id)
                coli.etat_embarquement=1
                coli.date_embarquement=datejour
                coli.heure_embarquement=heurejour
                coli.save()

        codembarquement=self.request.POST.get("codembarquement")
        poids_embarquement=self.request.POST.get("poids_embarquement")
        transporteur=self.request.POST.get("transporteurs")
        agence_arrive=self.request.POST.get("agence_arrive")
        datejour = date.today()
        heurejour = datetime.now()

        m=Embarquement.objects.create(codeembarquement=codembarquement,poids=poids_embarquement,nombre_lots=len(lots),dates=datejour,heure=heurejour,author_id=self.request.user.id,agence_depart_id=self.request.user.agences_id,agence_arrive_id=agence_arrive,transporteurs_id=transporteur)

        for k,v in lots.items():
            DetailEmbarquement.objects.create(embarquements_id=m.id,lots_id=v['id'])
            new_lot=Lot.objects.get(id=v['id'])
            new_lot.etat_embarqment=1
            new_lot.user_etat_embarqment_id=self.request.user.id
            new_lot.date_etat_embarqment=datejour
            new_lot.heure_etat_embarqment=heurejour
            new_lot.save()
            colis=Coli.objects.filter()

        CodeEmbarquement.objects.create()
        messages.success(self.request, "Lot ajouté avec succès")
        return super().post(request, *args, **kwargs)


class index(ListView):
    model = Embarquement
    template_name = 'embarquements/index.html'
    context_object_name = 'embarquements'



class edit(UpdateView):
    model = Embarquement
    form_class = EmbarquementEditForm
    template_name = 'embarquements/edit.html'
    success_url = reverse_lazy('embarquements-index')

    def form_valid(self, form):
        messages.success(self.request, "Modification éffectuée avec succès")
        return super().form_valid(form)


class detail_embarquement(DetailView):
    model = Embarquement
    template_name = 'embarquements/detail_embarquement.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lots"] = DetailEmbarquement.objects.filter(embarquements_id=self.kwargs["pk"]) 
        context["embarquement"] = self.get_object() 
        return context
    

    


   
    



