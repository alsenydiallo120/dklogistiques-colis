from django.views.generic import CreateView, ListView, DeleteView, UpdateView,DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from depots.models import Depot
from reglements.models import Reglement
from .models import Coli,CodeColis
from .forms import ColiForm,RapportForm
from num2words import num2words
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from entreprise.models import Entreprise
from django.db.models import Q,Sum
from django.shortcuts import render
from django.db import transaction
from tauxs.models import Taux
from django.conf import settings
from depenses.models import Depense
LINK=settings.LINK


class create(CreateView):
    model = Coli
    form_class = ColiForm
    template_name = 'colis/create.html'
    success_url = reverse_lazy('colis-index')

    def form_valid(self, form):
        poids=float(self.request.POST.get("poids"))
        prix=float(self.request.POST.get("prix"))
        
        montant=poids*prix

        montantpaye=float(self.request.POST.get("montant_paye"))
        devise=self.request.POST.get("devise")
        devise_montantpaye=self.request.POST.get("devise_montantpaye")

        taux_jour=Taux.objects.first().gnf

        if poids<1:poids=1
        montant=poids*prix

        if devise=="€" and devise_montantpaye=="€":
            prix_euro=prix
            reste=round((montant-montantpaye),2)

        if devise=="gnf" and devise_montantpaye=="gnf":
            montant_euro=round(montant/taux_jour,0)
            montantpaye=round(montantpaye/taux_jour,0)
            prix_euro=round(prix/taux_jour,0)
            reste=round((montant_euro-montantpaye),2)

        if devise=="gnf" and devise_montantpaye=="€":
            montant_euro=round(montant/taux_jour,0)
            prix_euro=round(prix/taux_jour,0)
            reste=round((montant_euro-montantpaye),2)
    

        form.instance.montant_euro=montant
        form.instance.montantpaye_euro=montantpaye
        form.instance.prix_euro=prix_euro
        form.instance.reste=reste
        form.instance.agence_depart_id=self.request.user.agences_id
        form.instance.author_id=self.request.user.id
        CodeColis.objects.create()
        messages.success(self.request, "Ajout éffectué avec succès")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
           code="V"+str(self.request.user.id)+"-A"+str(CodeColis.objects.count())
        else:
            code="V"+str(self.request.user.id)+"-"+str(CodeColis.objects.count())
        context['form']=ColiForm(initial={'code':code })
        return context


def find_colis(request):
    context={}
    if request.method=="POST":
        name=request.POST.get('name')
        colis=Coli.objects.filter(Q(code=name) | Q(tel_expeditaire=name) | Q(tel_destinataire=name)).first()
        if colis is not None:
            context['reste']=int(colis.montant)-int(colis.montant_paye)
            context['colis']=colis
        else:
            context['message']="Colis non trouvé"
        return render(request,"colis/find_colis.html",context)
    return render(request,"colis/find_colis.html",context)


def mon_rapport(request):
    context={}
    context['form']=RapportForm()
    if request.method=="POST":
        date1=request.POST.get('date1')
        date2=request.POST.get('date2')

        colis_entree_euro=Coli.objects.filter(agence_depart_id=request.user.agences_id,devise_montantpaye="€",dates__range=(date1,date2)).aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0
        colis_paye_euro=Reglement.objects.filter(agences_id=request.user.agences_id,devise="€",dates__range=(date1,date2)).aggregate(Sum('montant'))["montant__sum"] or 0

        colis_entree_gnf=Coli.objects.filter(agence_depart_id=request.user.agences_id,devise_montantpaye="gnf",dates__range=(date1,date2)).aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0
        colis_paye_gnf=Reglement.objects.filter(agences_id=request.user.agences_id,devise="gnf",dates__range=(date1,date2)).aggregate(Sum('montant'))["montant__sum"] or 0

        depenses=Depense.objects.filter(agences_id=request.user.agences_id,dates__range=(date1,date2)).aggregate(Sum('montant'))["montant__sum"] or 0

        depot_euro=Depot.objects.filter(agences_id=request.user.agences_id,devise="€",dates__range=(date1,date2)).aggregate(Sum('montant'))["montant__sum"] or 0

        depot_gnf=Depot.objects.filter(agences_id=request.user.agences_id,devise="gnf",dates__range=(date1,date2)).aggregate(Sum('montant'))["montant__sum"] or 0

        recette_euro=float(colis_entree_euro)+colis_paye_euro
        recette_gnf=float(colis_entree_gnf)+float(colis_paye_gnf)
        cisse_euro=float(colis_entree_euro)+float(colis_paye_euro)-float(depot_euro)
        cisse_gnf=float(colis_entree_gnf)+float(colis_paye_gnf)-float(depenses)-float(depot_gnf)
    

        context['recette_euro']=recette_euro
        context['recette_gnf']=recette_gnf
        context['cisse_euro']=cisse_euro
        context['cisse_gnf']=cisse_gnf
        context['depot_gnf']=depot_gnf
        context['depot_euro']=depot_euro
        context['depenses']=depenses

        return render(request,"colis/mon_rapport.html",context)
    return render(request,"colis/mon_rapport.html",context)

def print_facture(request,pk):
    pass
    context={}
    template_path = "colis/print.html"
    enreprise=Entreprise.objects.first()
    colis=Coli.objects.filter(id=pk).first()
    context['entreprise']=enreprise
    context['colis']=colis
    context['reste']=colis.reste
    context['range']= range(colis.nombre_colis)
    context['link']= LINK+"/API/scanner/"+str(pk)+"/"
    context['code']= colis.code+" | Exp:"+colis.expditaire+" | Dest:"+colis.destinataire
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="bon_de_livraison.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    

class index(ListView):
    model = Coli
    template_name = 'colis/index.html'
    context_object_name = 'colis'

class etat_colis(ListView):
    model = Coli
    template_name = 'colis/etats.html'
    context_object_name = 'colis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["colis"] = Coli.objects.filter(etat_receptionclient=0)
        return context
    

class edit(UpdateView):
    model = Coli
    form_class = ColiForm
    template_name = 'colis/edit.html'
    success_url = reverse_lazy('colis-index')

class detail(DetailView):
    model = Coli
    template_name = 'colis/detail.html'
    context_object_name = 'colis'


class delete(DeleteView):
    model = Coli
    template_name = 'colis/edit.html'
    success_url = reverse_lazy('colis-index')
    success_message = 'Suprression effectuee avec succes'

