from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Clientsrendezvou
from .forms import ClientsrendezvouForm
from django.db import transaction
from clients.models import Client
from django.http import HttpResponseRedirect



class create(CreateView):
	model = Clientsrendezvou
	form_class = ClientsrendezvouForm
	template_name = 'clientsrendezvous/create.html'
	success_url = reverse_lazy('rendezvous_du_jour')

	@transaction.atomic
	def form_valid(self, form):
		m=form.save()
		nb_client=Client.objects.filter(telephone=m.telephone).count()
		if nb_client==0:
			Client.objects.create(nom=m.nom,telephone=m.telephone)
		return HttpResponseRedirect("/rendezvous/rendezvous_du_jour")
	

class index(ListView):
	model = Clientsrendezvou
	template_name = 'clientsrendezvous/index.html'
	context_object_name = 'clientsrendezvous'




class edit(UpdateView):
	model = Clientsrendezvou
	form_class = ClientsrendezvouForm
	template_name = 'clientsrendezvous/edit.html'
	success_url = reverse_lazy('clientsrendezvous-index')

	# @transaction.atomic
	# def form_valid(self, form):
	# 	m=form.save()
	# 	nb_client=Client.objects.filter(telephone=m.telephone).count()
	# 	if nb_client==0:
	# 		Client.objects.create(nom=m.nom,telephone=m.telephone)
	# 	return HttpResponseRedirect("/rendezvous/rendezvous_du_jour")
	

class delete(DeleteView):
	model = Clientsrendezvou
	template_name = 'clientsrendezvous/edit.html'
	success_url = reverse_lazy('clientsrendezvous-index')
	success_message = 'Suprression effectuee avec succes'

