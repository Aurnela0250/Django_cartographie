from django.shortcuts import render, redirect, get_object_or_404
from .models import Etablissement, Utilisateur
from .forms import EtablissementForm
from django.contrib import messages 
from .forms import UtilisateurForm
from django.contrib.auth import login, authenticate
from rest_framework import viewsets
from .serializers import UtilisateurSerializer
from .serializers import EtablissementSerializer


def carte(request):
    etablissements = Etablissement.objects.all()
    print(etablissements)
    return render(request, '../templates/cartographie/carte.html', {'etablissements': etablissements})

# etablissement
def creer_etablissement(request):
    if request.method == 'POST':
        form = EtablissementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_etablissements')
    else:
        form = EtablissementForm()
    return render(request, 'cartographie/creer_etablissement.html', {'form': form})

def liste_etablissements(request):
    etablissements = Etablissement.objects.all()
    return render(request, 'cartographie/liste_etablissements.html', {'etablissements': etablissements})

def modifier_etablissement(request, id):
    etablissement = Etablissement.objects.get(id=id)
    if request.method == 'POST':
        form = EtablissementForm(request.POST, instance=etablissement)
        if form.is_valid():
            form.save()
            return redirect('liste_etablissements')
    else:
        form = EtablissementForm(instance=etablissement)
    return render(request, 'cartographie/modifier_etablissement.html', {'form': form})

def supprimer_etablissement(request, id):
    etablissement = Etablissement.objects.get(id=id)
    if request.method == 'POST':
        etablissement.delete()
        return redirect('liste_etablissements')
    return render(request, 'cartographie/supprimer_etablissement.html', {'etablissement': etablissement})

# utilisateur
def creer_utilisateur(request):
    if request.method == 'POST':
        form = UtilisateurForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.set_password(form.cleaned_data['mot_de_passe'])
            utilisateur.save()
            messages.success(request, 'Utilisateur créé avec succès.')
            return redirect('liste_utilisateurs')
    else:
        form = UtilisateurForm()
    return render(request, 'creer_utilisateur.html', {'form': form})

def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'liste_utilisateurs.html', {'utilisateurs': utilisateurs})

def modifier_utilisateur(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        form = UtilisateurForm(request.POST, instance=utilisateur)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.set_password(form.cleaned_data['mot_de_passe'])
            utilisateur.save()
            messages.success(request, 'Utilisateur modifié avec succès.')
            return redirect('liste_utilisateurs')
    else:
        form = UtilisateurForm(instance=utilisateur)
    return render(request, 'modifier_utilisateur.html', {'form': form})

def supprimer_utilisateur(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        utilisateur.delete()
        messages.success(request, 'Utilisateur supprimé avec succès.')
        return redirect('liste_utilisateurs')
    return render(request, 'supprimer_utilisateur.html', {'utilisateur': utilisateur})

def connexion(request):
    if request.method == 'POST':
        email = request.POST['email']
        mot_de_passe = request.POST['mot_de_passe']
        utilisateur = Utilisateur.objects.filter(email=email).first()
        if utilisateur and utilisateur.check_password(mot_de_passe):
            login(request, utilisateur)
            return redirect('accueil')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
    return render(request, 'connexion.html')


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

class EtablissementViewSet(viewsets.ModelViewSet):
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer