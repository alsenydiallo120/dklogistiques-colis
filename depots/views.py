from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Depot
from .forms import DepotForm
from datetime import date


class create(CreateView):
    model = Depot
    form_class = DepotForm
    template_name = 'depots/create.html'
    success_url = reverse_lazy('depots-index')

    def get_initial(self):
        initial = super().get_initial()
        initial['dates'] = date.today() 
        return initial

    def form_valid(self, form):
        form.instance.author_id=self.request.user.id
        form.instance.agences=self.request.user.agences
        messages.success(self.request, "Dépot éffectué avec succès")
        return super().form_valid(form)



class index(ListView):
    model = Depot
    template_name = 'depots/index.html'
    context_object_name = 'depots'

class edit(UpdateView):
    model = Depot
    form_class = DepotForm
    template_name = 'depots/edit.html'
    success_url = reverse_lazy('depots-index')

class delete(DeleteView):
    model = Depot
    template_name = 'depots/edit.html'
    success_url = reverse_lazy('depots-index')
    success_message = 'Suprression effectuee avec succes'

