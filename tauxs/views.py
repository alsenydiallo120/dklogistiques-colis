from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Taux
from .forms import TauxForm
from django.db import transaction
from accounts.models import CustomUser


class create(CreateView):
    model = Taux
    form_class = TauxForm
    template_name = 'tauxs/create.html'
    success_url = reverse_lazy('tauxs-index')

    @transaction.atomic
    def form_valid(self, form):
        gnf=self.request.POST.get("gnf")
        taux="1€="+gnf+" GNF"
        CustomUser.objects.update(taux_jour=taux,valeur_taux=gnf)
        form.instance.author_id=self.request.user.id
        form.save()
        return super().form_valid(form)


class index(ListView):
    model = Taux
    template_name = 'tauxs/index.html'
    context_object_name = 'tauxs'


class edit(UpdateView):
    model = Taux
    form_class = TauxForm
    template_name = 'tauxs/edit.html'
    success_url = reverse_lazy('tauxs-index')


class delete(DeleteView):
    model = Taux
    template_name = 'tauxs/edit.html'
    success_url = reverse_lazy('tauxs-index')
    success_message = 'Suprression effectuee avec succes'

