from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import CForm, RendezvouForm
from datetime import date
from entreprise.models import Entreprise
from num2words import num2words
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse, HttpResponseRedirect
from querystring_parser import parser
from django.db import transaction




class rendezvous_du_jour(ListView):
	model = Rendezvou
	template_name = 'rendezvous/index.html'
	context_object_name = 'rendezvous'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		datej=date.today()
		context["rendezvous"] = Rendezvou.objects.filter(dates=datej) 
		context["titre"] = "Les rendez-vous du jour" 
		context["imprimer"] = "imprimer" 
		return context


@transaction.atomic
def print_rendez_vous_jour(request):
    context={}
    datej=date.today()
    if request.method=="POST":
        chauffeur_id=request.POST.get("chauffeurs")
        rendez_vous = parser.parse(request.POST.urlencode())['rendez_vous']
        for k,r in rendez_vous.items():
            rdv=PriseRendezvou.objects.filter(
                  rendezvous_id=r["id"],
                  chauffeurs_id=chauffeur_id,
                  datejour=datej
                ).count()
            if rdv==0:
                PriseRendezvou.objects.create(
                    rendezvous_id=r["id"],
                    chauffeurs_id=chauffeur_id,
                    datejour=datej
                )
        redv=PriseRendezvou.objects.filter(datejour=datej,chauffeurs_id=chauffeur_id)
        context['datej']=datej
        context["entreprise"] = Entreprise.objects.first() 
        context["rendezvous"] =  redv
        context["impression"] =  redv.first()
        template_path = "rendezvous/rendezvous_du_jour.html"    
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="reglement.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


class create(CreateView):
    model = Rendezvou
    form_class = RendezvouForm
    template_name = 'rendezvous/create.html'
    success_url = reverse_lazy('rendezvous-index')


class index(ListView):
    model = Rendezvou
    template_name = 'rendezvous/index.html'
    context_object_name = 'rendezvous'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titre"] = "Liste des rendez-vous" 
        return context



class rendezvous_du_jour(ListView):
    model = Rendezvou
    template_name = 'rendezvous/index.html'
    context_object_name = 'rendezvous'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datej=date.today()
        prises=PriseRendezvou.objects.filter(datejour=datej).values_list("rendezvous_id",flat=True)
        context["rendezvous"] = Rendezvou.objects.filter(dates=datej).exclude(id__in=prises) 
        context["titre"] = "Les rendez-vous du jour" 
        context["imprimer"] = "imprimer" 
        context["chauffeur_form"] = CForm() 
        return context
    



class edit(UpdateView):
    model = Rendezvou
    form_class = RendezvouForm
    template_name = 'rendezvous/edit.html'
    success_url = reverse_lazy('rendezvous-index')



class delete(DeleteView):
    model = Rendezvou
    template_name = 'rendezvous/edit.html'
    success_url = reverse_lazy('rendezvous-index')
    success_message = 'Suprression effectuee avec succes'

