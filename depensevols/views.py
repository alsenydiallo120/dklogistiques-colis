
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib import messages
from datetime import date
from django.shortcuts import render



def add_depensevols(request):
    return render(request,"depensevols/add_depensevols.html")


class create(CreateView):
    model = Depensevol
    form_class = DepenseVolForm
    template_name = 'depensevols/create.html'
    success_url = reverse_lazy('depensevols-index')

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
    model = Depensevol
    template_name = 'depensevols/index.html'
    context_object_name = 'depensevols'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context["depensevols"] = Depensevol.objects.all().order_by("-id")
        else:
            context["depensevols"] = Depensevol.objects.filter(author_id=self.request.user.id).order_by("-id")
        return context
    

class edit(UpdateView):
    model = Depensevol
    form_class = DepenseVolForm
    template_name = 'depensevols/edit.html'
    success_url = reverse_lazy('depensevols-index')

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
    model = Depensevol
    template_name = 'depensevols/edit.html'
    success_url = reverse_lazy('depensevols-index')
    success_message = 'Suprression effectuee avec succes'

