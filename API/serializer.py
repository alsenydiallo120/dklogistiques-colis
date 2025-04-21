from rest_framework import serializers
from API.models import Demandedevis
from colis.models import Coli
from rendezvous.models import *


class ScannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coli
        fields = ["id"]


class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model=RendezvousMobile
        fields = ["nom","telephone","email","date","heure","description"]

  

class DemandeDevisSerializer(serializers.ModelSerializer):
    class Meta:
        model=Demandedevis
        exclude = ["slug"]

  
