from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Annee
from .forms import AnneeForm

class create(CreateView):
	model = Annee
	form_class = AnneeForm
	template_name = 'annees/create.html'
	success_url = reverse_lazy('annees-index')

class index(ListView):
	model = Annee
	template_name = 'annees/index.html'
	context_object_name = 'annees'

class edit(UpdateView):
	model = Annee
	form_class = AnneeForm
	template_name = 'annees/edit.html'
	success_url = reverse_lazy('annees-index')

class delete(DeleteView):
	model = Annee
	template_name = 'annees/edit.html'
	success_url = reverse_lazy('annees-index')
	success_message = 'Suprression effectuee avec succes'

