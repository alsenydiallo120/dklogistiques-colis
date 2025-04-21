from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import ClotureConteneurForm, ConteneurForm
from django.db import transaction
from django.http import HttpResponseRedirect



class create(CreateView):
	model = Conteneur
	form_class = ConteneurForm
	template_name = 'conteneurs/create.html'
	success_url = reverse_lazy('conteneurs-index')

	def get_initial(self):
		initial = super().get_initial()
		initial['code'] = str(RefConteneur.objects.count()).zfill(2)
		return initial

	@transaction.atomic
	def form_valid(self, form):
		RefConteneur.objects.create()
		messages.success(self.request, "conteneur ajouté avec succès")
		form.save()
		return HttpResponseRedirect("/conteneurs/")
		
	
class index(ListView):
	model = Conteneur
	template_name = 'conteneurs/index.html'
	context_object_name = 'conteneurs'


class edit(UpdateView):
	model = Conteneur
	form_class = ConteneurForm
	template_name = 'conteneurs/edit.html'
	success_url = reverse_lazy('conteneurs-index')


class cloturer(UpdateView):
	model = Conteneur
	form_class = ClotureConteneurForm
	template_name = 'conteneurs/cloturer.html'
	success_url = reverse_lazy('conteneurs-index')

	def form_valid(self, form):
		form.instance.cloture=True
		return super().form_valid(form)
	


class delete(DeleteView):
	model = Conteneur
	template_name = 'conteneurs/edit.html'
	success_url = reverse_lazy('conteneurs-index')
	success_message = 'Suprression effectuee avec succes'

