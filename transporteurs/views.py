from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Transporteur
from .forms import TransporteurForm

class create(CreateView):
	model = Transporteur
	form_class = TransporteurForm
	template_name = 'transporteurs/create.html'
	success_url = reverse_lazy('transporteurs-index')

class index(ListView):
	model = Transporteur
	template_name = 'transporteurs/index.html'
	context_object_name = 'transporteurs'

class edit(UpdateView):
	model = Transporteur
	form_class = TransporteurForm
	template_name = 'transporteurs/edit.html'
	success_url = reverse_lazy('transporteurs-index')

class delete(DeleteView):
	model = Transporteur
	template_name = 'transporteurs/edit.html'
	success_url = reverse_lazy('transporteurs-index')
	success_message = 'Suprression effectuee avec succes'

