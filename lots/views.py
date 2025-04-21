from django.views.generic import CreateView, ListView, DeleteView, UpdateView,DetailView
from django.urls import reverse_lazy
from .models import CodeLot, Lot, DetailLot
from .forms import LotForm
from colis.models import Coli
from querystring_parser import parser
from django.http import HttpResponse,HttpResponseRedirect
from datetime import date,datetime
from django.db import transaction
from django.contrib import messages

  
class create(CreateView):
    model = Lot
    form_class = LotForm
    template_name = 'lots/create.html'
    success_url = reverse_lazy('lots-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["colis"] = Coli.objects.filter(etat_lot=0,author=self.request.user.id)
        if self.request.user.is_superuser:
            coldelot="LDKLV"+str(self.request.user.id)+"-"+"ADM"+str(CodeLot.objects.count())
        else:
            coldelot="LDKLV"+str(self.request.user.id)+"-"+str(self.request.user.agences.pays.libelle)[0:1]+str(CodeLot.objects.count())
        context["codelot"] = coldelot 
        return context
        
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        colis = parser.parse(self.request.POST.urlencode())['colis']
        codelot=self.request.POST.get("codelot")
        poids_lot=self.request.POST.get("poids_lot")
        datejour = date.today()
        heurejour = datetime.now()
        m=Lot.objects.create(codelot=codelot,poids_lot=poids_lot,nombre_colis=len(colis),dates=datejour,heure=heurejour,author_id=self.request.user.id,agences_id=self.request.user.agences_id)

        for k,v in colis.items():
            DetailLot.objects.create(lots_id=m.id,colis_id=v['id'])
            new_coli=Coli.objects.get(id=v['id'])
            new_coli.etat_lot=1
            new_coli.heure_lot=heurejour
            new_coli.date_lot=datejour
            new_coli.user_lot_id=self.request.user.id
            new_coli.save()
        CodeLot.objects.create()
        messages.success(self.request, "Lot ajouté avec succès")
        return super().post(request, *args, **kwargs)

    
class index(ListView):
    model = Lot
    template_name = 'lots/index.html'
    context_object_name = 'lots'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lots"] = Lot.objects.filter(agences_id=self.request.user.agences.id,etat_embarqment=0) 
        return context
    

class edit(UpdateView):
    model = Lot
    form_class = LotForm
    template_name = 'lots/edit.html'
    success_url = reverse_lazy('lots-index')

class delete(DeleteView):
    model = Lot
    success_url = reverse_lazy('lots-index')
    success_message = 'Suprression effectuee avec succes'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        detail_lot=DetailLot.objects.filter(lots_id=self.kwargs['pk'])
        for d in detail_lot:
            coli=Coli.objects.get(id=d.colis_id)
            coli.etat_lot=0
            coli.date_lot=None
            coli.heure_lot=None
            coli.user_lot_id=None
            coli.save()
        return self.delete(request, *args, **kwargs)


class detail(DetailView):
    model = Lot
    context_object_name = 'lot'
    template_name = 'lots/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["colis"] = DetailLot.objects.filter(lots_id=self.kwargs['pk'])
        context["codelot"] = Lot.objects.get(id=self.kwargs['pk']).codelot
        return context
    

