from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from CGEI.my_functions import calcule_reste_vol_paris
from .models import *
from .forms import RegulationForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from entreprise.models import Entreprise
from num2words import num2words
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.db import transaction
from colis.models import Coli, ColiBateau
from decimal import Decimal
from django.db.models import Sum,Q
from datetime import date,datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from regulationbateaus.models import Regulationbateau




@csrf_exempt
def get_colis_regulation_bateau(request):
    datas = []
    q = request.GET.get("q", "")
    if q:
        colis = ColiBateau.objects.filter(Q(code__icontains=q)).exclude(etat_receptionclient=1).exclude(agence_depart__pays_id=1)
        for c in colis:
            datas.append({
                "id": c.id,
                "text": c.code
            })
    data = {"items": datas}
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def get_colis_regulations(request):
    datas = []
    q = request.GET.get("q", "")
    if q:
        colis = Coli.objects.filter(Q(code__icontains=q)).exclude(etat_receptionclient=1).exclude(agence_depart__pays_id=1)
        for c in colis:
            datas.append({
                "id": c.id,
                "text": c.code
            })
    data = {"items": datas}
    return JsonResponse(data, content_type="application/json", safe=False)




@csrf_exempt
def get_info_colis_regulation(request):
    context={}
    if request.method == 'POST':
        colis_id=request.POST.get("id_colis")
        coli=Coli.objects.get(id=colis_id)
        context["expditaire"]=coli.expditaire.nom
        context["destinataire"]=coli.destinataire.nom
        context["montant"]=coli.montant
        context["paye"]=float(coli.montant_paye)+float((Regulation.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0)),
        context["reste"]=float(coli.montant)-float(coli.montant_paye)-float((Regulation.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0))
        return JsonResponse(context, content_type="application/json",safe=False)



@csrf_exempt
def get_info_colis_regulation_bateau(request):
    context={}
    if request.method == 'POST':
        colis_id=request.POST.get("id_colis")
        coli=ColiBateau.objects.get(id=colis_id)
        context["expditaire"]=coli.expditaire.nom
        context["destinataire"]=coli.destinataire.nom
        context["montant"]=coli.montant
        context["paye"]=float(coli.montant_paye)+float((Regulationbateau.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0)),
        context["reste"]=float(coli.montant)-float(coli.montant_paye)-float((Regulationbateau.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0))
        return JsonResponse(context, content_type="application/json",safe=False)



class create(CreateView):
    model = Regulation
    form_class = RegulationForm
    template_name = 'regulations/create.html'
    success_url = reverse_lazy('regulations-index')

    def get_initial(self):
        initial = super().get_initial()
        annees_id=Annee.objects.last().id
        datej = date.today().strftime("%d/%m%y")
        initial['reference'] = "RV"+str(self.request.user.id)+str(datej)+str(ReferenceRegulation.objects.filter(annees_id=annees_id).count()+1)
        initial['pays'] = self.request.user.agences.pays.id
        return initial	

    @transaction.atomic
    def form_valid(self, form):
        form.instance.agences_id=self.request.user.agences.id
        form.instance.author_id=self.request.user.id
        m=form.save()
        annees_id=Annee.objects.last().id
        ReferenceRegulation.objects.create(annees_id=annees_id)
        calcule_reste_vol_paris(m.colis_id)
        messages.success(self.request, "Ajout effectué avec succès")
        return HttpResponseRedirect('/regulations/')
        
    


class index(ListView):
    model = Regulation
    template_name = 'regulations/index.html'
    context_object_name = 'regulations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context["regulations"] = Regulation.objects.order_by("-id")
        else:
            context["regulations"] = Regulation.objects.filter(author_id=self.request.user.id).order_by("-id")
        return context
    


class edit(UpdateView):
    model = Regulation
    form_class = RegulationForm
    template_name = 'regulations/edit.html'
    success_url = reverse_lazy('regulations-index')

    def get_initial(self):
        initial = super().get_initial()
        initial['pays'] = self.request.user.agences.pays.id
        return initial	


class delete(DeleteView):
    model = Regulation
    template_name = 'regulations/edit.html'
    success_url = reverse_lazy('regulations-index')
    success_message = 'Suprression effectuee avec succes'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        m=self.get_object()
        self.delete(request, *args, **kwargs)
        calcule_reste_vol_paris(m.colis_id)
        messages.success(self.request, 'Suppression effectuée')
        return HttpResponseRedirect("/regulations/")



@transaction.atomic
def regulations_print(request,pk):
    context={}
    datej=datetime.today()
    template_path = "regulations/print_recu.html"    
    impression = Regulation.objects.get(id=pk)
    entreprise=Entreprise.objects.first()
    colis=Coli.objects.get(id=impression.colis_id)
    montant=Decimal(colis.montant)
    montant_paye=Decimal(colis.montant_paye)
    reglement=Decimal(Regulation.objects.filter(colis_id=impression.colis_id).aggregate(Sum("montant"))["montant__sum"] or 0)
    reste=montant-montant_paye-reglement
    montant_lettre = num2words(impression.montant, lang='fr')
    context['datej']=datej
    context['nombre']=[1,2]
    context['entreprise']=entreprise
    context['impression']=impression
    context['reste']=reste
    context['montant_lettre']=montant_lettre
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="reglement.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


