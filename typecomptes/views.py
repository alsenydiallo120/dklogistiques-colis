from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Typecompte
from .forms import TypecompteForm

class create(CreateView):
	model = Typecompte
	form_class = TypecompteForm
	template_name = 'typecomptes/create.html'
	success_url = reverse_lazy('typecomptes-index')
	
	def form_valid(self, form):
		messages.success(self.request, f"Type {self.request.POST.get('libelle')} ajouté avec succcess")
		return super().form_valid(form)

class index(ListView):
	model = Typecompte
	template_name = 'typecomptes/index.html'
	context_object_name = 'typecomptes'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["typecomptes"] = Typecompte.objects.order_by('-id')
		return context
	

class edit(UpdateView):
	model = Typecompte
	form_class = TypecompteForm
	template_name = 'typecomptes/edit.html'
	success_url = reverse_lazy('typecomptes-index')
	
	def form_valid(self, form):
		messages.success(self.request, f"Type {self.request.POST.get('libelle')} modifié avec succcess")
		return super().form_valid(form)

class delete(DeleteView):
	model = Typecompte
	template_name = 'typecomptes/edit.html'
	success_url = reverse_lazy('typecomptes-index')
	success_message = 'Suprression effectuee avec succes'

