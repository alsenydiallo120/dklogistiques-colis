from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from CGEI.my_functions import *
from annees.models import Annee
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.views.generic import CreateView, DeleteView, UpdateView,ListView,DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db import transaction
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum
from django.core import serializers
from colis.models import Coli, ColiBateau
from tauxs.models import Taux
from django.http import HttpResponse
from decimal import Decimal
from entreprise.models import Entreprise
from num2words import num2words
from datetime import datetime,date




# @csrf_exempt
# def get_colis_info(request):
#     codes = []
#     q = request.GET.get("colis_id", "")
#     print("Q", q)
#     if q:
#         coli = Coli.objects.get(id=q)
#         codes.append({
#                 "expeditaire": coli.expditaire.nom,
#                 "destinataire": coli.destinataire.nom, 
#                 "montant": coli.montant,
#                 "paye":float(coli.montant_paye)+float((Regulation.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0)),
#                 "reste":float(coli.montant)-float(coli.montant_paye)-float((Regulation.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0))
#             })
#     data = {"items": codes}





@transaction.atomic
def reglements_print(request,pk):
    context={}
    datej=datetime.today()
    template_path = "reglements/print_recu.html"    
    impression = Reglement.objects.get(id=pk)
    entreprise=Entreprise.objects.first()
    montant_lettre_euro = num2words(impression.montant_euro or 0, lang='fr')
    montant_lettre_gnf = num2words(impression.montant_gnf or 0, lang='fr')
    context['datej']=datej
    context['nombre']=[1,2]
    context['entreprise']=entreprise
    context['impression']=impression
    context['user']=request.user
    context['montant_lettre_euro']=montant_lettre_euro
    context['montant_lettre_gnf']=montant_lettre_gnf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="reglement.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



@csrf_exempt
def get_colis_vol(request):
    datas = []
    q = request.GET.get("q", "")
    if q:
        colis=Coli.objects.filter(etat_receptionclient=0,code__icontains=q)
        for c in colis:
            datas.append({
                "id": c.id,
                "text": c.code
            })
    data = {"items": datas}
    return JsonResponse(data, content_type="application/json", safe=False)



@csrf_exempt
def get_reste(request):
    if request.method == 'POST':
        colis_id=request.POST.get("id_colis")
        colis=Coli.objects.get(id=colis_id)
        reglements_euro=Regulation.objects.filter(colis_id=colis_id).aggregate(Sum("montant"))["montant__sum"] or 0

        if colis.devise_montantpaye=="gnf":
            taux_jour=Taux.objects.last().gnf
            montant_paye_euro=colis.montant_paye/taux_jour
        else:
            montant_paye_euro=colis.montant_paye

        montant_paye=round(montant_paye_euro-Decimal(reglements_euro),2)
        reste=round(colis.montant-montant_paye_euro-Decimal(reglements_euro),2)
        context={}
        context['reste']=abs(reste)
        context['poids']=colis.poids
        context['prix_euro']=colis.prix
        context['nombre_colis']=colis.nombre_colis
        context['montant_euro']=colis.montant_euro
        context['contenu']=colis.contenu
        context['montant_paye']=montant_paye
        return JsonResponse(context, content_type="application/json",safe=False)



def reglements_add(request):
    return render(request,"reglements/reglements_add.html")



def update_colis_vol(request):
    colis=Coli.objects.all()
    colis_bateau=ColiBateau.objects.all()
    for c in colis:
        calcule_reste_vol_paris(c.id)
        
    for c in colis_bateau:
        calcule_reste_bateau(c.id)
    return HttpResponseRedirect("/reglements/")




class create(CreateView):
    model = Reglement
    form_class = ReglementForm
    template_name = 'reglements/create.html'
    success_url = reverse_lazy('reglements-index')

    def get_initial(self):
        initial = super().get_initial()
        annees_id=Annee.objects.last().id
        datej = date.today().strftime("%d/%m%y")
        initial['reference'] = "RV"+str(self.request.user.id)+str(datej)+str(ReferenceReception.objects.filter(annees_id=annees_id).count()+1)
        initial['agences_id'] = self.request.user.agences_id
        return initial	

    @transaction.atomic
    def form_valid(self, form):
        form.instance.author_id=self.request.user.id
        form.instance.agences_id=self.request.user.agences_id
        m=form.save()
        Coli.objects.filter(id=m.colis_id).update(etat_receptionclient=1)
        messages.success(self.request, "Paiement éffectué avec succès")
        return super().form_valid(form)



class create_guinee(CreateView):
    model = Reglement
    form_class = ReglementFormGuinee
    template_name = 'reglements/create_guinee.html'
    success_url = reverse_lazy('reglements-index')

    def get_initial(self):
        initial = super().get_initial()
        annees_id=Annee.objects.last().id
        datej = date.today().strftime("%d/%m%y")
        initial['reference'] = "RV"+str(self.request.user.id)+str(datej)+str(ReferenceReception.objects.filter(annees_id=annees_id).count()+1)
        initial['agences_id'] = self.request.user.agences_id
        return initial	
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        check_invalid_fields(form)
        return HttpResponse("")
    

    @transaction.atomic
    def form_valid(self, form):
        form.instance.author_id=self.request.user.id
        form.instance.agences_id=self.request.user.agences_id
        m=form.save()
        Coli.objects.filter(id=m.colis_id).update(etat_receptionclient=1)
        messages.success(self.request, "Paiement éffectué avec succès")
        return super().form_valid(form)



class create_bateau(CreateView):
    model = Reglement
    form_class = ReglementBateauForm
    template_name = 'reglements/create_bateau.html'
    success_url = reverse_lazy('reglements-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reglements"] = Reglement.objects.filter(colis=None,author=self.request.user.id)
        return context

    def get_initial(self):
        initial = super().get_initial()
        annees_id=Annee.objects.last().id
        datej = date.today().strftime("%d/%m%y")
        initial['reference'] = "RB"+str(self.request.user.id)+str(datej)+str(ReferenceReception.objects.filter(annees_id=annees_id).count()+1)
        return initial	

    @transaction.atomic
    def form_valid(self, form):
        form.instance.author_id=self.request.user.id
        form.instance.agences_id=self.request.user.agences_id
        m=form.save()
        ColiBateau.objects.filter(id=m.colisbateau_id).update(etat_receptionclient=1)
        messages.success(self.request, "Paiement éffectué avec succès")
        return super().form_valid(form)



class index(ListView):
    model = Reglement
    template_name = 'reglements/index.html'
    context_object_name = 'reglements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            context["reglements"] = Reglement.objects.select_related("colis","colisbateau","author").filter(author_id=self.request.user.id).order_by("-id")[:1000]
        else:
            context["reglements"] = Reglement.objects.select_related("colis","colisbateau","author").order_by("-id")[:1000]
        return context
    

class edit(UpdateView):
    model = Reglement
    form_class = ReglementForm
    template_name = 'reglements/edit.html'
    success_url = reverse_lazy('reglements-index')


class delete(DeleteView):
    model = Reglement
    template_name = 'reglements/edit.html'
    success_url = reverse_lazy('reglements-index')
    success_message = 'Suprression effectuee avec succes'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        colis_id=self.get_object().colis_id
        self.delete(request, *args, **kwargs)
        Coli.objects.filter(id=colis_id).update(etat_receptionclient=0)
        ColiBateau.objects.filter(id=colis_id).update(etat_receptionclient=0)
        messages.success(self.request, 'Suppression effectuee avec succes')
        return HttpResponseRedirect('/reglements/')
        


