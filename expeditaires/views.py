from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Expeditaire
from .forms import ExpeditaireForm

class create(CreateView):
	model = Expeditaire
	form_class = ExpeditaireForm
	template_name = 'expeditaires/create.html'
	success_url = reverse_lazy('expeditaires-index')

class index(ListView):
	model = Expeditaire
	template_name = 'expeditaires/index.html'
	context_object_name = 'expeditaires'

class edit(UpdateView):
	model = Expeditaire
	form_class = ExpeditaireForm
	template_name = 'expeditaires/edit.html'
	success_url = reverse_lazy('expeditaires-index')

class delete(DeleteView):
	model = Expeditaire
	template_name = 'expeditaires/edit.html'
	success_url = reverse_lazy('expeditaires-index')
	success_message = 'Suprression effectuee avec succes'

