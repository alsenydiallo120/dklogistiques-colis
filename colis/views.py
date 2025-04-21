from django.views.generic import CreateView, ListView, DeleteView, UpdateView,DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from depots.models import Depot
from reglements.models import Reglement
from .models import *
from .forms import *
from num2words import num2words
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse, HttpResponseRedirect
from entreprise.models import Entreprise
from django.db.models import Q,Sum
from django.shortcuts import render
from django.db import transaction
from tauxs.models import Taux
from django.conf import settings
from depenses.models import Depense
from clients.models import Client
from datetime import date
from agences.models import Agence
from clients.forms import ClientForm
from annees.models import Annee
from conteneurs.models import Conteneur
from CGEI.my_functions import *
from django.db.models import Q, F, Case, When, Value, IntegerField
from django.db.models.functions import Cast
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
LINK=settings.LINK



@csrf_exempt
def get_clients(request):
    destinataire = []
    q = request.GET.get("q", "")
    if q:
        results = Client.objects.filter(telephone__icontains=q)[:10]
        for client in results:
            destinataire.append({
                "id": client.id,
                "text": client.nom+" | "+client.telephone 
            })
    data = {"items": destinataire}
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def get_colis_reglement(request):
    datas = []
    q = request.GET.get("q", "")
    if q:
        colis = Coli.objects.filter(Q(code__icontains=q))[:10]
        for c in colis:
            datas.append({
                "id": c.id,
                "text": c.code
            })
    data = {"items": datas}
    return JsonResponse(data, content_type="application/json", safe=False)



@csrf_exempt
def get_codes_vol(request):
    codes = []
    q = request.GET.get("q", "")
    if q:
        pays=request.user.agences.pays.id
        results = Coli.objects.filter(code__icontains=q,etat_receptionclient=0,agence_depart__pays_id=pays)
        for coli in results:
            codes.append({
                "id": coli.id,
                "text": coli.code 
            })
    data = {"items": codes}
    return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def get_colis_info(request):
    codes = []
    q = request.GET.get("colis_id", "")
    print("Q", q)
    if q:
        coli = Coli.objects.get(id=q)
        codes.append({
                "expeditaire": coli.expditaire.nom,
                "destinataire": coli.destinataire.nom, 
                "montant": coli.montant,
                "paye":float(coli.montant_paye)+float((Regulation.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0)),
                "reste":float(coli.montant)-float(coli.montant_paye)-float((Regulation.objects.filter(colis_id=coli.id).aggregate(Sum("montant"))['montant__sum'] or 0))
            })
    data = {"items": codes}
    return JsonResponse(data, content_type="application/json", safe=False)




@transaction.atomic
def colis_add_item(request):
    context={}
    if request.method == "POST":
        colis_id=request.POST.get("colis")
        form = ColiDetailForm(request.POST)
        check_invalid_fields(form)
        if form.is_valid():
            if colis_id==None:
                form.instance.author_id=request.user.id
                form.save()
                colisdetail=DetaiColis.objects.filter(colis_id=None,author=request.user.id)
                context['items']=colisdetail
                context['total']=float(colisdetail.aggregate(Sum("montant"))["montant__sum"] or 0)
                return render(request, 'colis/items_list.html',context)
            else:
                form.instance.author_id=request.user.id
                form.instance.colis_id=colis_id
                form.save()
                items=DetaiColis.objects.filter(colis_id=colis_id)
                context['items']=items
                context['total']=float(items.aggregate(Sum("montant"))["montant__sum"] or 0)
                return render(request, 'colis/items_list.html',context)
    else:
        context['form'] = ColiDetailForm()
    return render(request, 'colis/items_list.html',context)




@transaction.atomic
def colis_delete_item(request,pk):
    context={}
    ids_colis=[]
    colis=DetaiColis.objects.filter(id=pk)
    colis_id=colis.first().colis_id
    ids_colis.append(colis_id)
    colis.delete()
    if ids_colis[0] is not None and DetaiColis.objects.filter(colis_id=ids_colis[0]).first() is not None:
        items=DetaiColis.objects.filter(colis_id=ids_colis[0])
    else:
        items=DetaiColis.objects.filter(colis_id=None,author_id=request.user.id)
    context['items']=items
    context['total']=float(items.aggregate(Sum("montant"))["montant__sum"] or 0)
    messages.success(request,'Suppression éffectuée avec succes')
    return render(request, 'colis/items_list.html',context)



def nouveau_client(request):
    form = ClientForm()
    return render(request, 'colis/nouveau_client.html', {
        'client_form': form,
    })


def get_destinataire(request):
    context={}
    telephone=request.GET.get("expditaire")
    telephone_destinataire=Coli.objects.filter(tel_expeditaire=telephone).values_list("tel_destinataire",flat=True).distinct()
    destinataires=Coli.objects.filter(tel_destinataire__in=telephone_destinataire).values_list
    context["destinataires"]=destinataires
    return render(request, "colis/select_destinataire.html",context)



class create(CreateView):
    model = Coli
    form_class = ColiForm
    template_name = 'colis/create.html'
    success_url = reverse_lazy('colis-index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug=self.request.GET.get("vlslug")
        type=self.request.GET.get("type")
        desti=self.request.GET.get("destinataire")
        clt=self.request.GET.get("client")
        client=Client.objects.filter(slug=slug).first()
        id_destinataires=0
        if client is not None:
            context["client"]=client
            id_destinataires=Coli.objects.filter(expditaire_id=client.id).values_list("destinataire_id",flat=True)
        context["type"]=type
        context["slug"]=slug
        context["desti"]=desti
        context["clt"]=clt
        context["clients"]=Client.objects.filter(id__in=id_destinataires)
        context['expditaire'] = Client.objects.filter(slug=slug).first().id
        return context

    def get_initial(self):
        initial = super().get_initial()
        user_agences = self.request.user.agences
        slug=self.request.GET.get("vlslug")
        id_destinataire=Attribution.objects.filter(expditaire__slug=slug).values_list("destinataire",flat=True)
        if user_agences is not None:
            initial['pays'] = user_agences.pays.libelle if user_agences.pays else None
            initial['code'] = user_agences.libelle[0] + str(self.request.user.id) + "-" + str(CodeColis.objects.count())
        else:
            initial['pays'] = None
            initial['code'] = "DefaultCode" 
        initial['slug'] = slug 
        return initial

    @transaction.atomic
    def form_valid(self, form):
        taux=Taux.objects.first().gnf
        form.instance.agence_depart_id=self.request.user.agences_id
        form.instance.author_id=self.request.user.id
        form.instance.taux=taux
        form.instance.types="Vol"
        form.instance.agence_depart_id=self.request.user.agences_id
        form.instance.dates=date.today()
        form.instance.destinataire_id=self.request.POST.get("destinataire")
        form.instance.expditaire_id=self.request.POST.get("expditaire")
        CodeColis.objects.create()
        m=form.save()
        calcule_reste_vol_paris(m.id)
        messages.success(self.request, "Ajout éffectué avec succès")
        return HttpResponseRedirect("/colis/")

  

class create_bateau(create):
    model=ColiBateau
    form_class=ColiBateauForm
    template_name = 'colis/create_bateau.html'
    success_url = reverse_lazy('colis-create_bateau')
    
    def dispatch(self, request, *args, **kwargs):
        conteneur=Conteneur.objects.filter(cloture=False).last()
        if conteneur==None:
            messages.error(self.request,"-")
            return HttpResponseRedirect("/clients/send_colis")
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        user_agences = self.request.user.agences
        slug=self.request.GET.get("vlslug")
        id_destinataire=Attribution.objects.filter(expditaire__slug=slug).values_list("destinataire",flat=True)
        lettre=Annee.objects.last().lettre
        conteneur=""
        conteneur=Conteneur.objects.filter(cloture=False).last()
        if conteneur is not None:
            conteneur_id=conteneur.id
            initial['conteneurs'] = conteneur_id
        initial['expditaire'] = Client.objects.filter(slug=slug).first().id
        if user_agences is not None:
            initial['pays'] = user_agences.pays.libelle if user_agences.pays else None
            initial['code'] =lettre+ str(self.request.user.id)+"-"+ str(CodeColisBateau.objects.filter(conteneurs_id=conteneur_id).count()+1).zfill(3)+"-"+str(conteneur.code)
        else:
            initial['pays'] = None
            initial['code'] = "DefaultCode" 
        initial['slug'] = slug 
        initial['id_destinataire'] = id_destinataire 
        initial['devise_montantpaye'] = "€" 
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug=self.request.GET.get("vlslug")
        type=self.request.GET.get("type")
        client=Client.objects.filter(slug=slug).first()
        id_destinataires=0
        if client is not None:
            context["client"]=client
            id_destinataires=Coli.objects.filter(expditaire_id=client.id).values_list("destinataire_id",flat=True)
        context["type"]=type
        context["slug"]=slug
        context["clients"]=Client.objects.filter(id__in=id_destinataires)
        context["detailform"]=ColiDetailForm()
        coli=DetaiColis.objects.filter(author_id=self.request.user.id,colis_id=None)
        context["items"] = coli
        context["items_count"] = coli.count()
        context['total']=float(coli.aggregate(Sum("montant"))["montant__sum"] or 0)
        return context

    @transaction.atomic
    def form_valid(self, form):
        dc=DetaiColis.objects.filter(author_id=self.request.user.id,colis_id=None)
        slug=self.request.GET.get("vlslug")
        type=self.request.GET.get("type")
        if dc.count()==0:
            messages.error(self.request,"-")
            return HttpResponseRedirect(f"/colis/create_bateau?vlslug={slug}&type={type}")
        else:
            montant=float(dc.aggregate(Sum("montant"))["montant__sum"] or 0)
            taux=Taux.objects.first().gnf
            frais=float(self.request.POST.get("frais") or 0)
            montant=montant+frais
            form.instance.agence_depart_id=self.request.user.agences_id
            form.instance.author_id=self.request.user.id
            form.instance.taux=taux
            form.instance.montant=montant
            form.instance.types="Bateau"
            form.instance.agence_depart_id=self.request.user.agences_id
            form.instance.dates=date.today()
            m=form.save()
            CodeColisBateau.objects.create(conteneurs_id=m.conteneurs_id)
            dc.update(colis_id=m.id)
            calcule_reste_bateau(m.id)
            messages.success(self.request, "Ajout éffectué avec succès")
            return HttpResponseRedirect("/colis/bateau")

    


def find_colis(request):
    context={}
    if request.method=="POST":
        name=request.POST.get('name')
        colis_vol=Coli.objects.filter(Q(code=name)).first()
        colis_bateau=ColiBateau.objects.filter(Q(code=name)).first()
        if colis_vol==None and colis_bateau==None:
            messages.error(request, f"Aucun colis correspondant au code <span style='color:#028FC5;font-weight:bold' >{name}</span> n'a été trouvé")
        else:
            reste=[]
            if colis_vol is not None:
                data=calcule_reste_vol_paris(colis_vol.id)
                context['colis']=colis_vol
            elif colis_bateau is not None:
                data=calcule_reste_bateau_paris(colis_vol.id)
                context['colis']=colis_bateau
            else:
                context['message']="Colis non trouvé"
            context['reste']=data[0]
            context['montant_paye']=data[1]
        return render(request,"colis/find_colis.html",context)
    return render(request,"colis/find_colis.html",context)



def valide_colis_bateau(request,pk):
    ColiBateau.objects.filter(id=pk).update(etat_verification=1)
    return HttpResponseRedirect("/colis/bateau")
     
    
def remove_validate_colis_bateau(request,pk):
    ColiBateau.objects.filter(id=pk).update(etat_verification=0)
    return HttpResponseRedirect("/colis/bateau")
     


def mon_rapport(request):
    context={}
    context['form']=RapportForm()
    return render(request,"colis/mon_rapport.html",context)



def print_rapport(request):
    context={}
    context['form']=RapportForm()
    if request.method=="POST":
        date1=request.POST.get('date1')
        date2=request.POST.get('date2')
        datejour=date.today()
        agences=request.user.agences_id
        colis_gnf_vol=Coli.objects.filter(dates__range=(date1,date2),agence_depart_id=agences,devise_montantpaye="gnf")
        colis_euro_vol=Coli.objects.filter(dates__range=(date1,date2),agence_depart_id=agences,devise_montantpaye="€").exclude(montant_paye=0.00)
        colis_euro_bateau=ColiBateau.objects.filter(dates__range=(date1,date2),devise_montantpaye="€",agence_depart_id=agences)
        # ------------------------------------COLIS RECUPERES----------------------------------------
        colis_recupereres_vol_gnf=Reglement.objects.filter(~Q(montant_gnf='00'),~Q(montant_gnf='0'),~Q(montant_gnf=None),~Q(montant_gnf=""),dates__range=(date1,date2),colisbateau_id=None,agences_id=agences)
        colis_recupereres_vol_euro = Reglement.objects.filter(~Q(montant_euro='00'),~Q(montant_euro='0'),~Q(montant_euro=None),~Q(montant_euro=""),dates__range=(date1,date2),colisbateau_id=None,agences_id=agences)
        colis_recupereres_beteau_gnf=Reglement.objects.filter(~Q(montant_gnf='00'),~Q(montant_gnf='0'),~Q(montant_gnf=None),~Q(montant_gnf=""),dates__range=(date1,date2),colis_id=None,agences_id=agences)
        colis_recupereres_beteau_euro=Reglement.objects.filter(~Q(montant_euro='00'),~Q(montant_euro='0'),~Q(montant_euro=None),~Q(montant_euro=""),dates__range=(date1,date2),colis_id=None,agences_id=agences)
        # ---------------------------------------DEPENSES-----------------------------------------
        depenses_vol_gnf=Depensevol.objects.filter(dates__range=(date1,date2), agences_id=agences,devise="gnf")
        depenses_vol_euro=Depensevol.objects.filter(dates__range=(date1,date2), agences_id=agences,devise="€")
        depenses_bateau_gnf=Depense.objects.filter(dates__range=(date1,date2),agences_id=agences,devise="gnf")
        depenses_bateau_euro=Depense.objects.filter(dates__range=(date1,date2),devise="€")
        #----------------------colis-------------------------------
        context["colis_gnf_vol"]=colis_gnf_vol
        context["colis_euro_vol"]=colis_euro_vol
        context["colis_euro_bateau"]=colis_euro_bateau
        context["colis_recupereres_vol_gnf"]=colis_recupereres_vol_gnf
        context["colis_recupereres_vol_euro"]=colis_recupereres_vol_euro
        context["colis_recupereres_beteau_gnf"]=colis_recupereres_beteau_gnf
        context["colis_recupereres_beteau_euro"]=colis_recupereres_beteau_euro
        #----------------------depenses----------------------------
        total_depenses_vol_gnf=depenses_vol_gnf.aggregate(Sum("montant"))["montant__sum"] or 0
        total_depenses_bateau_gnf=depenses_bateau_gnf.aggregate(Sum("montant"))["montant__sum"] or 0
        total_depenses_vol_euro=float(depenses_vol_euro.aggregate(Sum("montant"))["montant__sum"] or 0)
        total_depenses_bateau_euro=float(depenses_bateau_euro.aggregate(Sum("montant"))["montant__sum"] or 0)
        #----------------------context----------------------------
        total_colis_recupereres_euro_vol=colis_recupereres_vol_euro.aggregate(Sum("montant_euro"))["montant_euro__sum"] or 0
        total_colis_recupereres_gnf_vol=colis_recupereres_vol_gnf.aggregate(Sum("montant_gnf"))["montant_gnf__sum"] or 0
        #----------------------context----------------------------
        total_colis_recupereres_euro_bateau=colis_recupereres_beteau_euro.aggregate(Sum("montant_euro"))["montant_euro__sum"] or 0
        total_colis_recupereres_gnf_bateau=colis_recupereres_beteau_gnf.aggregate(Sum("montant_gnf"))["montant_gnf__sum"] or 0
        #----------------------context----------------------------
        context["total_colis_recupereres_euro_vol"]=total_colis_recupereres_euro_vol
        context["total_colis_recupereres_gnf_vol"]=int(total_colis_recupereres_gnf_vol)
        context["total_colis_recupereres_euro_bateau"]=total_colis_recupereres_euro_bateau
        context["total_colis_recupereres_gnf_bateau"]=int(total_colis_recupereres_gnf_bateau)
        #----------------------context----------------------------
        context["depenses_vol_gnf"]=depenses_vol_gnf
        context["depenses_bateau_gnf"]=depenses_bateau_gnf
        context["depenses_vol_euro"]=depenses_vol_euro
        context["depenses_bateau_euro"]=depenses_bateau_euro
        #----------------------Totaux----------------------------
        context["total_depenses_vol_gnf"]=total_depenses_vol_gnf
        context["total_depenses_bateau_gnf"]=total_depenses_bateau_gnf
        context["total_depenses_vol_euro"]=0
        context["total_depenses_bateau_euro"]=0
        context["total_sortie_gnf"]=total_depenses_vol_gnf
        context["total_sortie_euro"]=0
        #----------------------Totaux colis vol------------------------------
        total_colis_euro_vol=float(colis_euro_vol.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
        total_colis_gnf_vol=float(colis_gnf_vol.aggregate(Sum('montant_paye'))["montant_paye__sum"] or 0)
        total_euro_vol=total_colis_euro_vol+total_colis_recupereres_euro_vol
        total_gnf_vol=total_colis_gnf_vol+total_colis_recupereres_gnf_vol
        #--------------------------------------------------------------------
        context["total_colis_gnf_vol"]=int(total_colis_gnf_vol)
        context["total_colis_euro_vol"]=total_colis_euro_vol
        context["total_euro_vol"]=total_euro_vol
        context["total_gnf_vol"]=total_gnf_vol
        #---------------------------------CAISSES VOL-----------------------------------
        context["caisse_gnf_vol"]=float(total_gnf_vol)-float(total_depenses_vol_gnf)
        context["caisse_euro_vol"]=total_euro_vol-total_depenses_vol_euro
        #---------------------------------CAISSES BATEAU-----------------------------------
        context["caisse_gnf_bateau"]=float(total_colis_recupereres_gnf_bateau)-float(total_depenses_bateau_gnf)
        context["caisse_euro_bateau"]=total_euro_vol-total_depenses_vol_euro
        context["agence"]=Agence.objects.get(id=agences)
        context["colis"] = Coli.objects.filter(dates=date.today())
        context["datejour"]=datejour
        context["date1"]=convert_date_courte(date1)
        context["date2"]=convert_date_courte(date2)
        context["entreprise"]=Entreprise.objects.first()
        context["total_euro_vol"]=total_euro_vol
        template_path = "colis/print_rapport.html"
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="bon_de_livraison.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response





def print_facture(request,pk):
    context={}
    template_path = "colis/print.html"
    enreprise=Entreprise.objects.first()
    colis=Coli.objects.filter(id=pk).first()

    if colis.devise=="€" and colis.devise_montantpaye=="€":
        montant_p=colis.montant_paye
        reste=colis.montant-colis.montant_paye
        montant=colis.montant

    if colis.devise=="€" and colis.devise_montantpaye=="gnf":
        montant_p=int(colis.montant_paye)
        payer=int(colis.montant_paye)/int(colis.taux)
        reste=round(float(colis.montant)-payer)
        montant=colis.montant

    if colis.devise=="gnf" and colis.devise_montantpaye=="gnf":
        montant_p=int(colis.montant_paye)
        reste_gnf=int(colis.montant)-int(colis.montant_paye)
        reste=round(int(reste_gnf)/int(colis.taux))
        montant=int(colis.montant)

    if colis.devise=="gnf" and colis.devise_montantpaye=="€":
        montant_p=int(colis.montant_paye)
        montant_gnf=int(colis.montant)/int(colis.taux)
        reste_euro=montant_gnf-montant_p
        reste=round(reste_euro)
        montant=int(colis.montant)
    
    context['paye']=montant_p
    context['montant']=montant
    context['entreprise']=enreprise
    context['colis']=colis
    context['reste']=reste
    context['range']= range(1,colis.nombre_colis+1)
    context['nbcolis']= colis.nombre_colis
    context['qr']= colis.code
    context['code']= colis.code+" | Exp:"+str(colis.expditaire or "")+" | Dest:"+str(colis.destinataire or "")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="bon_de_livraison.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def print_list_colis_conteneur(request):
    context={}
    if request.method=="POST":
        conteneur=request.POST.get("conteneurs")
        type=request.POST.get("type")
        colis=ColiBateau.objects.filter(conteneurs_id=conteneur)
        detail_colis=DetaiColis.objects.filter(colis__conteneurs_id=conteneur)

        datas={}
        for c in colis:
            data={}
            data["code"]=c.code
            dcs={}
            for d in detail_colis:
                dc={}
                if c.id==d.colis_id:
                    dc['designation']=d.designation
                    dc['quantite']=d.quantite_detail
                    dcs[d.id]=dc
            data["detail"]=dcs
            data["rowspan"]=len(dcs)
            datas[c.id]=data

        context["detail_colis"]=detail_colis
        context["colis"]=colis
        context["datas"]=datas
        context["conteneur"]=Conteneur.objects.get(id=conteneur)
        context["entreprise"]=Entreprise.objects.first()
        if type=="Imprimer avec la liste des clients":
            template_path = "colis/print_list_colis_conteneur.html"
        else:
            template_path = "colis/print_list_colis_transitaire.html"
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'filename=f"bon_de_livraison.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




def print_facture_bateau(request,pk):
    context={}
    template_path = "colis/print_bateau.html"
    enreprise=Entreprise.objects.first()
    colis=ColiBateau.objects.filter(id=pk).first()
    montant=colis.montant
    if colis.devise=="€" and colis.devise_montantpaye=="€":
        montant_p=colis.montant_paye
        reste=montant-colis.montant_paye

    if colis.devise=="€" and colis.devise_montantpaye=="gnf":
        montant_p=int(colis.montant_paye)
        payer=int(colis.montant_paye)/int(colis.taux)
        reste=round(float(montant)-payer)

    if colis.devise=="gnf" and colis.devise_montantpaye=="gnf":
        montant_p=int(colis.montant_paye)
        reste_gnf=int(montant)-int(colis.montant_paye)
        reste=round(int(reste_gnf)/int(colis.taux))

    if colis.devise=="gnf" and colis.devise_montantpaye=="€":
        montant_p=int(colis.montant_paye)
        montant_gnf=int(montant)/int(colis.taux)
        reste_euro=montant_gnf-montant_p
        reste=round(reste_euro)
        # montant=int(colis.montant)

    detail_colis=DetaiColis.objects.filter(colis_id=pk)
    context['paye']=montant_p
    context['montant']=float(montant or 0)
    context['frais']=colis.frais  
    context['entreprise']=enreprise
    context['colis']=colis
    context['items']=detail_colis
    context['reste']=reste
    context['range']= range(1,detail_colis.count()+1)
    context['nbcolis']= detail_colis.count()
    context['qr']= colis.code
    context['link']= LINK+"/API/scanner/"+str(pk)+"/"
    context['code']= colis.code+" | Exp:"+str(colis.expditaire or "")+" | Dest:"+str(colis.destinataire or "")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="bon_de_livraison.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

    

class index(ListView):
    model = Coli
    template_name = 'colis/index.html'
    context_object_name = 'colis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code=self.request.GET.get("code")
        if code is not None:
            context["colis"]=Coli.objects.filter(Q(code=code) | Q(expditaire__telephone__icontains=code) | Q(destinataire__telephone__icontains=code)).order_by("-id")
        else:
            context["colis"]=Coli.objects.filter(agence_depart_id=self.request.user.agences.id).select_related("expditaire","destinataire","agence_depart").order_by("-id")[:100]
        context['pays'] = self.request.user.agences.pays.id
        return context




# def filter_colis(request):
#     context={}
#     mot=request.GET.get("mot")
#     print("MOT ", mot)
#     colis=Coli.objects.filter(code__icontains=mot)
#     context["colis_vol"]=colis
#     return render(request,"colis/index_htmx.html", context)



def filter_colis(request):
    context = {}
    mot = request.GET.get("mot", "")
    if len(mot) >= 5:
        colis = Coli.objects.filter(code__icontains=mot)
    else:
        colis=Coli.objects.all()[:100]
    context["colis_vol"] = colis
    return render(request, "colis/index_htmx.html", context)



class bateau(ListView):
    model = ColiBateau
    template_name = 'colis/bateau.html'
    context_object_name = 'colis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"]=ConteneurPrintForm()
        # context["colis"] = ColiBateau.objects.all()
        context["colis"] = ColiBateau.objects.select_related("agence_depart","agence_arrive","expditaire","destinataire","user_lot","user_embarquement")
        return context





class etat_colis(ListView):
    model = Coli
    template_name = 'colis/etats.html'
    context_object_name = 'colis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["colis"] = Coli.objects.filter(etat_receptionclient=0)
        return context
    

class edit(UpdateView):
    model = Coli
    form_class = EditColiForm
    template_name = 'colis/edit.html'
    success_url = reverse_lazy('colis-index')

    # def get_initial(self):
    #     initial = super().get_initial()
    #     user_agences = self.request.user.agences
    #     slug=self.request.GET.get("vlslug")
    #     id_destinataire=Attribution.objects.filter(expditaire__slug=slug).values_list("destinataire",flat=True)
    #     initial['expditaire'] = Client.objects.filter(slug=slug).first().id
    #     if user_agences is not None:
    #         initial['pays'] = user_agences.pays.libelle if user_agences.pays else None
    #         initial['code'] = user_agences.libelle[0] + str(self.request.user.id) + "-" + str(CodeColis.objects.count())
    #     else:
    #         initial['pays'] = None
    #         initial['code'] = "DefaultCode" 
    #     initial['slug'] = slug 
    #     initial['id_destinataire'] = id_destinataire 
    #     return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients']=Client.objects.all()
        return context
    



class edit_colis_bateau(UpdateView):
    model = ColiBateau
    form_class = ColiBateauForm
    template_name = 'colis/edit_colis_bateau.html'
    success_url = reverse_lazy('colis-index')

    def get_initial(self):
        initial = super().get_initial()
        user_agences = self.request.user.agences
        slug=self.request.GET.get("vlslug")
        id_destinataire=Attribution.objects.filter(expditaire__slug=slug).values_list("destinataire",flat=True)
        lettre=Annee.objects.last().lettre
        conteneur=""
        conteneur=Conteneur.objects.filter(cloture=False).last()
        if conteneur is not None:
            conteneur_id=conteneur.id
            initial['conteneurs'] = conteneur_id
        if user_agences is not None:
            initial['pays'] = user_agences.pays.libelle if user_agences.pays else None
        else:
            initial['pays'] = None
        initial['slug'] = slug 
        initial['id_destinataire'] = id_destinataire 
        return initial
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug=self.request.GET.get("vlslug")
        type=self.request.GET.get("type")
        client=Client.objects.filter(slug=slug).first()
        if client is not None:
            context["client"]=client
        context["type"]=type
        context["slug"]=slug
        coli=DetaiColis.objects.filter(colis_id=self.kwargs["pk"])
        context["items"] = coli
        context['total']=float(coli.aggregate(Sum("montant"))["montant__sum"] or 0)
        context["detailform"] = ColiDetailForm(
            initial={
                'colis':self.kwargs["pk"]
            }
        )
        return context

    @transaction.atomic
    def form_valid(self, form):
        dc=DetaiColis.objects.filter(author_id=self.request.user.id,colis_id=None)
        montant=dc.aggregate(Sum("montant"))["montant__sum"] or 0
        taux=Taux.objects.first().gnf
        form.instance.agence_depart_id=self.request.user.agences_id
        form.instance.author_id=self.request.user.id
        form.instance.taux=taux
        form.instance.montant=montant
        form.instance.types="Bateau"
        form.instance.agence_depart_id=self.request.user.agences_id
        form.instance.dates=date.today()
        m=form.save()
        CodeColisBateau.objects.create(conteneurs_id=m.conteneurs_id)
        dc.update(colis_id=m.id)
        messages.success(self.request, "Ajout éffectué avec succès")
        return HttpResponseRedirect("/colis/bateau")




class detail(DetailView):
    model = Coli
    template_name = 'colis/detail.html'
    context_object_name = 'colis'

class delete(DeleteView):
    model = Coli
    template_name = 'colis/edit.html'
    success_url = reverse_lazy('colis-index')
    success_message = 'Suprression effectuee avec succes'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        m=self.get_object()
        self.delete(request, *args, **kwargs)
        calcule_reste_vol_paris(m.id)
        messages.success(self.request, 'Suppression effectuée')
        return HttpResponseRedirect("/colis/")




class delete_colis_bateau(DeleteView):
    model = ColiBateau
    template_name = 'colis/edit.html'
    success_url = reverse_lazy('colis-bateau')
    
    def form_valid(self, form):
        m=self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        calcule_reste_bateau(m.id)
        messages.success(self.request,'Suppression éffectuée avec succes')
        return HttpResponseRedirect(success_url)


