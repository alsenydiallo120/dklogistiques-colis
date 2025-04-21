from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Destinataire
from .forms import DestinataireForm


class create(CreateView):
	model = Destinataire
	form_class = DestinataireForm
	template_name = 'destinataires/create.html'
	success_url = reverse_lazy('destinataires-index')


class index(ListView):
	model = Destinataire
	template_name = 'destinataires/index.html'
	context_object_name = 'destinataires'



class edit(UpdateView):
	model = Destinataire
	form_class = DestinataireForm
	template_name = 'destinataires/edit.html'
	success_url = reverse_lazy('destinataires-index')


class delete(DeleteView):
	model = Destinataire
	template_name = 'destinataires/edit.html'
	success_url = reverse_lazy('destinataires-index')
	success_message = 'Suprression effectuee avec succes'

