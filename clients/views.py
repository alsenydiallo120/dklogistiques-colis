from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Client
from .forms import ClientForm
from django.db import transaction
from colis.models import Attribution



class send_colis(ListView):
	model = Client
	template_name = 'clients/send_colis.html'
	context_object_name = 'clients'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		telephone=self.request.GET.get("telephone")
		if telephone is not None:
			context["clients"] = Client.objects.filter(telephone=telephone)
		else: 
			context["clients"] = Client.objects.order_by("-id")[:50] 
		context['pays'] = self.request.user.agences.pays.id
		return context
	

class create(CreateView):
	model = Client
	form_class = ClientForm
	template_name = 'clients/create.html'
	success_url = reverse_lazy('clients-index')


class create_new(create):
	success_url = reverse_lazy('send_colis')


class add_new_destinataire(create):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

	@transaction.atomic
	def form_valid(self, form):
		slug=self.request.GET.get("vlslug")
		type=self.request.GET.get("type")
		m=form.save()
		client=m.nom+" "+m.telephone
		expeditaire=Client.objects.filter(slug=slug).first()
		if expeditaire is not None:
			Attribution.objects.create(
				expditaire_id=expeditaire.id,
				destinataire_id=m.id
			)
		return HttpResponseRedirect(f"/colis/create/?vlslug={slug}&type={type}&destinataire={m.id}&client={client}")



class add_new_destinataire_bateau(add_new_destinataire):
	@transaction.atomic
	def form_valid(self, form):
		slug=self.request.GET.get("vlslug")
		type=self.request.GET.get("type")
		m=form.save()
		expeditaire=Client.objects.filter(slug=slug).first()
		if expeditaire is not None:
			Attribution.objects.create(
				expditaire_id=expeditaire.id,
				destinataire_id=m.id
			)
		return HttpResponseRedirect('/colis/create_bateau/?vlslug=%s&type=%s' % (slug, type))



		
	



class index(ListView):
	model = Client
	template_name = 'clients/index.html'
	context_object_name = 'clients'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["clients"] = Client.objects.order_by("-id")[:100] 
		return context
	


class edit(UpdateView):
	model = Client
	form_class = ClientForm
	template_name = 'clients/edit.html'
	success_url = reverse_lazy('clients-index')


class edit_from_colis(edit):
	success_url = reverse_lazy('send_colis')


class delete(DeleteView):
	model = Client
	template_name = 'clients/edit.html'
	success_url = reverse_lazy('clients-index')
	success_message = 'Suprression effectuee avec succes'

