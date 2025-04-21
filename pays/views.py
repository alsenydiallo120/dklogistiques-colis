from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Pay
from .forms import PayForm

class create(CreateView):
	model = Pay
	form_class = PayForm
	template_name = 'pays/create.html'
	success_url = reverse_lazy('pays-index')

class index(ListView):
	model = Pay
	template_name = 'pays/index.html'
	context_object_name = 'pays'

class edit(UpdateView):
	model = Pay
	form_class = PayForm
	template_name = 'pays/edit.html'
	success_url = reverse_lazy('pays-index')

class delete(DeleteView):
	model = Pay
	template_name = 'pays/edit.html'
	success_url = reverse_lazy('pays-index')
	success_message = 'Suprression effectuee avec succes'

