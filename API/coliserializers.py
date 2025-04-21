from rest_framework import serializers
from colis.models import *


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields = ['nom','telephone','email']



class ColiSerializer(serializers.ModelSerializer):
    expditaire = ClientSerializer()
    destinataire = ClientSerializer()
    class Meta:
        model=Coli
        fields = "__all__"



class ColiBateauSerializer(serializers.ModelSerializer):
    expditaire = ClientSerializer()
    destinataire = ClientSerializer()
    class Meta:
        model=ColiBateau
        fields = "__all__"



class ScannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coli
        fields = "__all__"
