from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Count,Q
from django.views import View
from depenses.models import Depense
from entreprise.models import Entreprise
from django.http import HttpResponseRedirect
from colis.models import Coli
from datetime import date
from django.shortcuts import render
from reglements.models import Reglement
from .forms import *
from django.db.models import Sum
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from datetime import date
from .my_functions import *
from datetime import date
from colis.models import ColiBateau
from regulations.models import Regulation
from depensevols.models import Depensevol
from decimal import Decimal
from regulationbateaus.models import *
from accounts.models import CustomUser






def dashboard_admin(request):
    context={}
    utilisateurs_parirs=CustomUser.objects.filter(agences__pays__libelle__icontains="france").exclude(is_superuser=True)
    admins=CustomUser.objects.filter(is_superuser=True)

    comptes_admins={}
    total_caisse_admin=0
    for u in admins:
        compte_admin={}
        caisse=caisse_admin_paris(u.id)
        compte_admin["nom"]=u.nom
        compte_admin["telephone"]=u.telephone
        compte_admin["caisse"]=caisse
        compte_admin["icone"]="bi bi-wallet2"
        comptes_admins[u.id]=compte_admin
        total_caisse_admin+=caisse
    context["comptes_admins"]=comptes_admins
    context["total_caisse_admin"]=total_caisse_admin
    comptes={}
    total_caisse=0
    for u in utilisateurs_parirs:
        compte={}
        caisse=caisse_paris_general(u.id)
        compte["nom"]=u.nom
        compte["telephone"]=u.telephone
        compte["caisse"]=caisse
        comptes[u.id]=compte
        total_caisse+=caisse
    context["comptes"]=comptes
    context["total"]=total_caisse
    return render(request,"dashboard_admin.html",context)




class rapport_jour_paris(FormView):
    form_class = RapportForm  
    template_name = 'rapports/rapport_jour_paris.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datejour=date.today()
        agences=self.request.user.agences_id
        colis_vol=Coli.objects.filter(dates=datejour,author_id=self.request.user.id, agence_depart_id=agences,devise_montantpaye="€")
        colis_bateau=ColiBateau.objects.filter(dates=datejour,author_id=self.request.user.id,devise_montantpaye="€")
        colis_recupereres=Reglement.objects.filter(dates=datejour,author_id=self.request.user.id)
        depenses_vol=Depensevol.objects.filter(dates=datejour,author_id=self.request.user.id, agences_id=agences,devise="€")
        depenses_bateau=Depense.objects.filter(dates=datejour,author_id=self.request.user.id,devise="€")
        reglements=Regulation.objects.filter(dates=datejour,author_id=self.request.user.id)
        reglements_bateau=Regulationbateau.objects.filter(dates=datejour,author_id=self.request.user.id)
        #----------------------colis-------------------------------
        context["colis_vol"]=colis_vol
        context["colis_bateau"]=colis_bateau
        context["colis_recupereres"]=colis_recupereres
        context["reglements"]=reglements
        context["reglements_bateau"]=reglements_bateau
        #----------------------depenses----------------------------
        total_depenses_vol=depenses_vol.aggregate(Sum("montant"))["montant__sum"] or 0
        total_depenses_bateau=depenses_bateau.aggregate(Sum("montant"))["montant__sum"] or 0
        total_colis_recupereres=colis_recupereres.aggregate(Sum("montant_euro"))["montant_euro__sum"] or 0
        total_vol=float(colis_vol.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
        total_colis_bateau=float(colis_bateau.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
        reglement_du_jour=float(reglements.aggregate(Sum('montant'))["montant__sum"] or 0)
        reglement_bateau_du_jour=float(reglements_bateau.aggregate(Sum('montant'))["montant__sum"] or 0)
        total=total_colis_bateau+total_vol+total_colis_recupereres+reglement_du_jour+reglement_bateau_du_jour
        #----------------------context----------------------------
        context["total_colis_recupereres"]=total_colis_recupereres
        context["depenses_vol"]=depenses_vol
        context["depenses_bateau"]=depenses_bateau
        context["reglement_bateau_du_jour"]=reglement_bateau_du_jour
        #----------------------Totaux----------------------------
        context["total_depenses_vol"]=total_depenses_vol
        context["total_depenses_bateau"]=total_depenses_bateau
        context["total_sortie"]=total_depenses_vol+total_depenses_bateau
        context["total"]=total
        context["caisse"]=Decimal(total)-Decimal(total_depenses_vol)-Decimal(total_depenses_bateau)
        context["agence"]=Agence.objects.get(id=agences)
        context["colis"] = Coli.objects.filter(dates=date.today())
        context["datejour"]=datejour
        context["total_vol"]=total_vol
        context["total_colis_bateau"]=total_colis_bateau
        context["reglement_du_jour"]=reglement_du_jour
        return context
    


class rapport_jour(FormView):
    form_class = RapportForm  
    template_name = 'rapports/rapport_jour.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datejour=date.today()
        agences=self.request.user.agences_id
        colis_gnf_vol=Coli.objects.filter(dates=datejour,author_id=self.request.user.id, agence_depart_id=agences,devise_montantpaye="gnf")
        colis_euro_vol=Coli.objects.filter(dates=datejour,author_id=self.request.user.id, agence_depart_id=agences,devise_montantpaye="€")
        colis_euro_bateau=ColiBateau.objects.filter(dates=datejour,author_id=self.request.user.id,devise_montantpaye="€")
        # ------------------------------------COLIS RECUPERES----------------------------------------
        colis_recupereres_euro=Reglement.objects.filter(dates=datejour,author_id=self.request.user.id)
        colis_recupereres_gnf=Reglement.objects.filter(~Q(montant_euro=00),~Q(montant_euro=0),dates=datejour,author_id=self.request.user.id)
        
        depenses_vol_gnf=Depensevol.objects.filter(dates=datejour,author_id=self.request.user.id, agences_id=agences,devise="gnf")
        depenses_bateau_gnf=Depense.objects.filter(dates=datejour,author_id=self.request.user.id,agences_id=agences,devise="gnf")
        #----------------------colis-------------------------------
        context["colis_gnf_vol"]=colis_gnf_vol
        context["colis_euro_vol"]=colis_euro_vol
        context["colis_euro_bateau"]=colis_euro_bateau
        context["colis_recupereres_euro"]=colis_recupereres_euro
        context["colis_recupereres_gnf"]=colis_recupereres_gnf
        #----------------------depenses----------------------------
        total_depenses_vol_gnf=depenses_vol_gnf.aggregate(Sum("montant"))["montant__sum"] or 0
        total_depenses_bateau_gnf=depenses_bateau_gnf.aggregate(Sum("montant"))["montant__sum"] or 0
        total_colis_recupereres_euro=colis_recupereres_euro.aggregate(Sum("montant_euro"))["montant_euro__sum"] or 0
        total_colis_recupereres_gnf=colis_recupereres_gnf.aggregate(Sum("montant_gnf"))["montant_gnf__sum"] or 0
        #----------------------context----------------------------
        context["total_colis_recupereres_euro"]=total_colis_recupereres_euro
        context["total_colis_recupereres_gnf"]=int(total_colis_recupereres_gnf)
        context["depenses_vol_gnf"]=depenses_vol_gnf
        context["depenses_bateau_gnf"]=depenses_bateau_gnf
        #----------------------Totaux----------------------------
        context["total_depenses_vol_gnf"]=total_depenses_vol_gnf
        context["total_depenses_bateau_gnf"]=total_depenses_bateau_gnf
        context["total_sortie_gnf"]=total_depenses_vol_gnf+total_depenses_bateau_gnf
        total_gnf_1=int(colis_gnf_vol.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
        total_euro_vol=float(colis_euro_vol.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
        total_colis_euro_bateau=float(colis_euro_bateau.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
        total_euro=total_colis_euro_bateau+total_euro_vol+total_colis_recupereres_euro
        total_gnf=total_colis_recupereres_gnf+total_gnf_1
        context["total_euro"]=total_euro
        context["total_gnf"]=total_gnf
        context["total_gnf_1"]=total_gnf_1
        context["caisse_gnf"]=float(total_gnf)-float(total_depenses_vol_gnf)-float(total_depenses_bateau_gnf)
        context["caisse_euro"]=total_euro
        context["agence"]=Agence.objects.get(id=agences)
        context["colis"] = Coli.objects.filter(dates=date.today())
        context["datejour"]=datejour
        context["total_euro_vol"]=total_euro_vol
        return context


    



class rapports(FormView):
    template_name = "rapports/rapport.html"
    form_class = RapportForm   

    def form_valid(self, form):
        context = self.get_context_data()
        rapports={}
        date_debut=self.request.POST.get("date_debut")
        date_fin=self.request.POST.get("date_fin")
        agences=self.request.POST.get("agences")
        types=self.request.POST.get("types")
        agent=self.request.POST.get("agent",0)

        q_objects = Q()
        q_objects_depense = Q()
        q_objects_reglement = Q()

        if date_debut and date_fin:
            q_objects &= Q(dates__range=(date_debut,date_fin))
            q_objects_reglement &= Q(dates__range=(date_debut,date_fin))
        if types!="":
            q_objects &=Q(types=types)
        if agent!="":
            q_objects &=Q(author_id=agent)
            q_objects_reglement &= Q(author_id=agent)
        q_objects_depense=q_objects
        if agences!="":
            q_objects &=Q(agence_depart_id=agences)
            q_objects_depense &=Q(agences_id=agences)
            q_objects_reglement &= Q(agences_id=agences)

        colis_recupereres_euro=Reglement.objects.filter(q_objects_reglement)
        colis_euro_vol=Coli.objects.filter(q_objects,devise_montantpaye="€")
        colis_euro_bateau=ColiBateau.objects.filter(q_objects,devise_montantpaye="€")
        depenses=Depense.objects.filter(dates__range=(date_debut,date_fin),author_id=agent,agences_id=agences)
        depenses_euro=depenses.filter(devise="€")
        #----------------------colis-------------------------------
        context["colis_euro_vol"]=colis_euro_vol
        context["colis_euro_bateau"]=colis_euro_bateau
        context["colis_recupereres_euro"]=colis_recupereres_euro
        # context["total_colis_recupereres_euro"]=total_colis_recupereres_euro
        #--------------------------------------------------
        total_colis_recupereres_euro=colis_recupereres_euro.aggregate(Sum("montant_euro"))["montant_euro__sum"] or 0
        total_depenses_euro=depenses_euro.aggregate(Sum("montant"))["montant__sum"] or 0
        total_colis_euro_bateau=float(colis_euro_bateau.aggregate(Sum("montant_paye"))["montant_paye__sum"] or 0)
        #--------------------------------------------------
        context["depenses_euro"]=depenses_euro
        context["total_depenses_euro"]=total_depenses_euro
        context["total_sortie_euro"]=total_depenses_euro
        context["total_colis_euro_bateau"]=total_colis_euro_bateau
        #----------------------Totaux----------------------------
        total_euro_vol=float(colis_euro_vol.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
        colis_euro_vol=float(colis_euro_vol.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
        total_euro=total_colis_euro_bateau+total_euro_vol+total_colis_recupereres_euro
        context["total_euro"]=total_euro
        context["caisse_euro"]=total_euro-total_depenses_euro
        context["agence"]=Agence.objects.get(id=agences)
        context["colis"] = Coli.objects.filter(dates=date.today())
        context["date_debut"]=convert_date_courte(date_debut)
        context["date_fin"]=convert_date_courte(date_fin)
        context["types"]=types
        context["agence"]=Agence.objects.get(id=agences)
       
        # if 'imprimer' in self.request.POST:
        #     template_path = "rapports/print_rapport.html"
        #     response = HttpResponse(content_type='application/pdf')
        #     response['Content-Disposition'] = 'filename="location.pdf"'
        #     template = get_template(template_path)
        #     html = template.render(context)
        #     pisa_status = pisa.CreatePDF(html, dest=response)
        #     if pisa_status.err:
        #         return HttpResponse('We had some errors <pre>' + html + '</pre>')
        #     return response
        # else:
        return self.render_to_response(context)




@login_required
def home(request):
    context={}
    datejour = date.today()
    agences=request.user.agences_id
    colis_vol=Coli.objects.filter(dates=datejour,author_id=request.user.id, agence_depart_id=agences,devise_montantpaye="€")
    colis_bateau=ColiBateau.objects.filter(dates=datejour,author_id=request.user.id,devise_montantpaye="€")
    colis_recupereres=Reglement.objects.filter(dates=datejour,author_id=request.user.id)
    depenses_vol=Depensevol.objects.filter(dates=datejour,author_id=request.user.id, agences_id=agences,devise="€")
    depenses_bateau=Depense.objects.filter(dates=datejour,author_id=request.user.id,devise="€")
    reglements=Regulation.objects.filter(dates=datejour,author_id=request.user.id)
    #----------------------colis-------------------------------
    context["colis_vol"]=colis_vol
    context["colis_bateau"]=colis_bateau
    context["colis_recupereres"]=colis_recupereres
    context["reglements"]=reglements
    #----------------------depenses----------------------------
    total_depenses_vol=depenses_vol.aggregate(Sum("montant"))["montant__sum"] or 0
    total_depenses_bateau=depenses_bateau.aggregate(Sum("montant"))["montant__sum"] or 0
    total_colis_recupereres=colis_recupereres.aggregate(Sum("montant_euro"))["montant_euro__sum"] or 0
    total_vol=float(colis_vol.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
    total_colis_bateau=float(colis_bateau.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
    reglement_du_jour=float(reglements.aggregate(Sum('montant'))["montant__sum"] or 0)
    total=total_colis_bateau+total_vol+total_colis_recupereres+reglement_du_jour
    #----------------------context----------------------------
    context["total_colis_recupereres"]=total_colis_recupereres
    context["depenses_vol"]=depenses_vol
    context["depenses_bateau"]=depenses_bateau
    #----------------------Totaux----------------------------
    context["total_depenses_vol"]=total_depenses_vol
    context["total_depenses_bateau"]=total_depenses_bateau
    context["total_sortie"]=total_depenses_vol+total_depenses_bateau
    context["total"]=total
    context["caisse"]=Decimal(total)-Decimal(total_depenses_vol)-Decimal(total_depenses_bateau)
    context["agence"]=Agence.objects.get(id=agences)
    context["colis"] = Coli.objects.filter(dates=date.today())
    context["datejour"]=datejour
    context["total_vol"]=total_vol
    context["total_colis_bateau"]=total_colis_bateau
    context["reglement_du_jour"]=reglement_du_jour
    colis_euro_bateau=ColiBateau.objects.filter(dates=datejour,author_id=request.user.id,devise_montantpaye="€").aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
    context['entreprise'] = Entreprise.objects.first()
    context["montant_gnf"]=int(Coli.objects.filter(author_id=request.user.id, agence_depart_id=request.user.agences_id,devise_montantpaye="gnf",dates=datejour).aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0)
    context["montant_euro"]=(Coli.objects.filter(author_id=request.user.id, agence_depart_id=request.user.agences_id,devise_montantpaye="€",dates=datejour).aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0)+colis_euro_bateau
    context["depense_jour"]=Depense.objects.filter(author_id=request.user.id, agences_id=request.user.agences_id,dates=datejour).aggregate(Sum('montant'))['montant__sum'] or 0
    context["nbcolis"]=Coli.objects.filter(author_id=request.user.id, agence_depart_id=request.user.agences_id,dates=datejour).count()
    if request.user.is_superuser:
        return HttpResponseRedirect("/tauxs/create/")
    else:
        return render(request,'home.html',context)





    