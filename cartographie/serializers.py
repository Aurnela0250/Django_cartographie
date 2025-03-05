from rest_framework import serializers
from .models import Utilisateur, Etablissement

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'nom', 'prenom', 'email', 'role']
        extra_kwargs = {'mot_de_passe': {'write_only': True}}

    def create(self, validated_data):
        utilisateur = Utilisateur.objects.create(**validated_data)
        utilisateur.set_password(validated_data['mot_de_passe'])
        utilisateur.save()
        return utilisateur
    
class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = ['id', 'nom', 'latitude', 'longitude', 'type', 'description']

    def create(self, validated_data):
        etablissement = Etablissement.objects.create(**validated_data)
        etablissement.save()
        return etablissement
