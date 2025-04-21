from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Agence
from .forms import AgenceForm

class create(CreateView):
	model = Agence
	form_class = AgenceForm
	template_name = 'agences/create.html'
	success_url = reverse_lazy('agences-index')

class index(ListView):
	model = Agence
	template_name = 'agences/index.html'
	context_object_name = 'agences'

class edit(UpdateView):
	model = Agence
	form_class = AgenceForm
	template_name = 'agences/edit.html'
	success_url = reverse_lazy('agences-index')

class delete(DeleteView):
	model = Agence
	template_name = 'agences/edit.html'
	success_url = reverse_lazy('agences-index')
	success_message = 'Suprression effectuee avec succes'

