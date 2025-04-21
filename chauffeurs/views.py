from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Chauffeur
from .forms import ChauffeurForm


class create(CreateView):
	model = Chauffeur
	form_class = ChauffeurForm
	template_name = 'chauffeurs/create.html'
	success_url = reverse_lazy('chauffeurs-create')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["chauffeurs"] = Chauffeur.objects.all()
		return context
	



class index(ListView):
	model = Chauffeur
	template_name = 'chauffeurs/index.html'
	context_object_name = 'chauffeurs'

class edit(UpdateView):
	model = Chauffeur
	form_class = ChauffeurForm
	template_name = 'chauffeurs/edit.html'
	success_url = reverse_lazy('chauffeurs-create')

class delete(DeleteView):
	model = Chauffeur
	template_name = 'chauffeurs/edit.html'
	success_url = reverse_lazy('chauffeurs-create')
	success_message = 'Suprression effectuee avec succes'

