from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from CGEI.my_functions import calcule_reste_bateau, calcule_reste_vol_paris
from .models import *
from .forms import RegulationbateauForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse, HttpResponseRedirect
from entreprise.models import Entreprise
from num2words import num2words
from datetime import datetime
from django.db import transaction
from colis.models import Coli
from decimal import Decimal
from django.db.models import Sum
from datetime import date,datetime




class create(CreateView):
    model = Regulationbateau
    form_class = RegulationbateauForm
    template_name = 'regulationbateaus/create.html'
    success_url = reverse_lazy('regulationbateaus-index')

    def get_initial(self):
        initial = super().get_initial()
        annees_id=Annee.objects.last().id
        datej = date.today().strftime("%d/%m%y")
        initial['reference'] = "RB"+str(self.request.user.id)+str(datej)+str(ReferenceRegulationBateau.objects.filter(annees_id=annees_id).count()+1)
        initial['pays'] = self.request.user.agences.pays.id
        return initial
    
    @transaction.atomic
    def form_valid(self, form):
        form.instance.agences_id=self.request.user.agences.id
        form.instance.author_id=self.request.user.id
        m=form.save()
        annees_id=Annee.objects.last().id
        ReferenceRegulationBateau.objects.create(annees_id=annees_id)
        calcule_reste_bateau(m.colis_id)
        messages.success(self.request, "Ajout effectué avec succès")
        return HttpResponseRedirect('/regulations/')

    


class index(ListView):
    model = Regulationbateau
    template_name = 'regulationbateaus/index.html'
    context_object_name = 'regulationbateaus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context["regulationbateaus"] = Regulationbateau.objects.order_by("-id")
        else:
            context["regulationbateaus"] = Regulationbateau.objects.filter(author_id=self.request.user.id).order_by("-id")
        return context
    


class edit(UpdateView):
    model = Regulationbateau
    form_class = RegulationbateauForm
    template_name = 'regulationbateaus/edit.html'
    success_url = reverse_lazy('regulationbateaus-index')

    def get_initial(self):
        initial = super().get_initial()
        initial['pays'] = self.request.user.agences.pays.id
        return initial



class delete(DeleteView):
    model = Regulationbateau
    template_name = 'regulationbateaus/edit.html'
    success_url = reverse_lazy('regulationbateaus-index')
    success_message = 'Suprression effectuee avec succes'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        m=self.get_object()
        self.delete(request, *args, **kwargs)
        calcule_reste_bateau(m.colis_id)
        messages.success(self.request, 'Suppression effectuée')
        return HttpResponseRedirect("/regulationbateaus/")



@transaction.atomic
def regulationbateaus_print(request,pk):
    context={}
    datej=datetime.today()
    template_path = "regulationbateaus/print_recu.html"    
    impression = Regulationbateau.objects.get(id=pk)
    entreprise=Entreprise.objects.first()
    colis=ColiBateau.objects.get(id=impression.colis_id)
    montant=Decimal(colis.montant)
    montant_paye=Decimal(colis.montant_paye)
    reglement=Decimal(Regulationbateau.objects.filter(colis_id=impression.colis_id).aggregate(Sum("montant"))["montant__sum"] or 0)
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


