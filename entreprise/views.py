from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from django.db.models import Sum
from .forms import EntrepriseForm
from .models import Entreprise
from django.urls import reverse_lazy

class create(CreateView):
    model = Entreprise
    form_class=EntrepriseForm
    success_url = reverse_lazy('entreprise-index')
    template_name = "entreprise/create.html"

class index(ListView):
    model = Entreprise
    template_name = "entreprise/index.html"
    context_object_name = "entreprises"



class edit(UpdateView):
    model = Entreprise
    template_name = "entreprise/edit.html"
    form_class = EntrepriseForm
    context_object_name = "entreprise"
    success_url = reverse_lazy('entreprise-index')












































        # sommedepot = Depot.objects.filter(compte_id=idcompte).aggregate(Sum('montant'))['montant__sum']
#         if sommedepot is None:
#             sommedepot = 0
#         sommeretrait = Retrait.objects.filter(compte_id=idcompte).aggregate(Sum('montant'))['montant__sum']
#         if sommeretrait is None:
#             sommeretrait = 0
#         sommetransfert = Transfert.objects.filter(idenvoi_id=idcompte).aggregate(Sum('montant'))['montant__sum']
#         if sommetransfert is None:
#             sommetransfert = 0
#         resultat = int(depot)+int(sommedepot)-int(sommeretrait)-int(sommetransfert)
#         statutcnpte = Statuscompte.objects.filter(types=types)
#         lastdte = Moncompte.objects.filter(compte_id=idcompte).order_by('id')[:1]
#         tdte = 0
#         for las in lastdte:
#             t = las.date
#             tdte = t.month
#         for stat in statutcnpte:
#             fraistenue = stat.faistenuecompte
#         if "Courant" in types:
#            if resultat > 0:
#                if delta == 1:
#                    Moncompte.objects.create(montant=fraistenue,date=datesys,compte_id=idcompte)
#                elif tdte - datetime.now().date().month == 1:
#                    Moncompte.objects.create(montant=fraistenue,date=datesys,compte_id=idcompte)
#         if "Morale" in types:
#            if resultat > 0:
#                if delta == 1:
#                    Moncompte.objects.create(montant=fraistenue,date=datesys,compte_id=idcompte)
#                elif tdte - datetime.now().date().month == 1:
#                    Moncompte.objects.create(montant=fraistenue,date=datesys,compte_id=idcompte)
#         if "DAT" in types:
#             if libelle == 5000000:
#                  pass
                   
#     return HttpResponse('bien')
    # return render(request, "moncomptes/index.html")
