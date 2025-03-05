from django import forms
from .models import Etablissement
from .models import Utilisateur, Role

class EtablissementForm(forms.ModelForm):
    class Meta:
        model = Etablissement
        fields = ['nom', 'latitude', 'longitude', 'type', 'description']


class UtilisateurForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    confirmer_mot_de_passe = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'role']

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmer_mot_de_passe = cleaned_data.get("confirmer_mot_de_passe")

        if mot_de_passe != confirmer_mot_de_passe:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")