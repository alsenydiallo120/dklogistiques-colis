from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Scanner
from .serializer import *
from .coliserializers import *
from colis.models import *
from rest_framework.response import Response
from django.http import HttpResponse
from datetime import date,datetime
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from django.db import transaction
from django.core.mail import send_mail





class liste_rendez_vous(generics.ListAPIView):
    queryset=RendezvousMobile.objects.all()
    serializer_class=RendezVousSerializer


class list_demande_devis(generics.ListAPIView):
    queryset=Demandedevis.objects.all()
    serializer_class=DemandeDevisSerializer


def convert_date_courte(date):
    dates=datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
    return dates

class add_rendez_vous(generics.CreateAPIView):
    queryset=RendezvousMobile.objects.all()
    serializer_class=RendezVousSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        m=serializer.save()
        message = (
            f"{m.description}\n\n"
            f"Cordialement,\n"
            f"Nom: {m.nom}\n"
            f"Tél: {m.telephone}\n"
            f"Email: {m.email}\n"
            f"Date du rendez-vous : {convert_date_courte(str(m.date))} à {m.heure}\n"
        )
        send_mail(
            "Demande de rendez-vous (DK LOGISTIQUE)",
            message,
            m.email,
            [m.email, "contact@dklogistique.com"],
        )


       




class add_demande_devis(generics.CreateAPIView):
    queryset=Demandedevis.objects.all()
    serializer_class=DemandeDevisSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        m=serializer.save()

        message = (
            f"{m.description}\n\n"
            f"Cordialement,\n\n"
            f"Nom: {m.nom}\n"
            f"Tél: {m.telephone}\n"
            f"Email: {m.email}\n"
            f"Adresse: {m.adresse}\n"
            f"Poids: {m.poids} Kg\n"
        )

        send_mail(
            "Demande de devis (DK LOGISTIQUE)",
            message,
            m.email,
            [m.email, "contact@dklogistique.com"],
        )


      





class get_coli_info(APIView):
    lookup_field = 'code'
    def get(self, request, code):
        try:
            coli = Coli.objects.get(code=code)
            serializer = ColiSerializer(coli)
            return Response(serializer.data)
        except Coli.DoesNotExist:
            pass
        try:
            colibateau = ColiBateau.objects.get(code=code)
            serializer = ColiBateauSerializer(colibateau)
            return Response(serializer.data)
        except ColiBateau.DoesNotExist:
            raise NotFound("Aucun colis trouvé avec ce code.")




@api_view(['GET'])
def scanner(request,pk):
    datejour = date.today()
    heurejour = datetime.now()
    coli=Coli.objects.filter(id=pk,etat_verification=0).first()
    if coli is not None:
        coli.etat_verification=1
        coli.date_verification=datejour
        coli.heure_verification=heurejour
        coli.save()
        respon={
            'res':True,
            }
        return Response(respon)
    else:
        respon={
            'res':False,
        }
        return Response(respon)
