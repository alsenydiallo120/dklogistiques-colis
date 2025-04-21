
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Depense
from .forms import DepenseForm
from django.contrib import messages
from datetime import date
from django.shortcuts import render



def add_depenses(request):
    return render(request,"depenses/add_depenses.html")


class create(CreateView):
    model = Depense
    form_class = DepenseForm
    template_name = 'depenses/create.html'
    success_url = reverse_lazy('depenses-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['typeuser'] = self.request.user.types
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['typeuser'] = self.request.user.types
        initial['role'] = self.request.user.is_superuser
        return initial

    def form_valid(self, form):
        form.instance.author_id=self.request.user.id
        form.instance.agences_id=self.request.user.agences_id
        form.instance.devise="€"
        messages.success(self.request, "Ajout éffectué avec succès")
        return super().form_valid(form)




class index(ListView):
    model = Depense
    template_name = 'depenses/index.html'
    context_object_name = 'depenses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context["depenses"] = Depense.objects.all().order_by("-id")
        else:
            context["depenses"] = Depense.objects.filter(author_id=self.request.user.id).order_by("-id")
        return context
    

class edit(UpdateView):
    model = Depense
    form_class = DepenseForm
    template_name = 'depenses/edit.html'
    success_url = reverse_lazy('depenses-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['typeuser'] = self.request.user.types
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['typeuser'] = self.request.user.types
        initial['role'] = self.request.user.is_superuser
        return initial


class delete(DeleteView):
    model = Depense
    template_name = 'depenses/edit.html'
    success_url = reverse_lazy('depenses-index')
    success_message = 'Suprression effectuee avec succes'

