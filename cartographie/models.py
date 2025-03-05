from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Etablissement(models.Model):
    nom = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    type = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom

class Role(models.Model):
    nomRole = models.CharField(max_length=200)

    def __str__(self):
        return self.nomRole

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def set_password(self, raw_password):
        self.mot_de_passe = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.mot_de_passe)

    def __str__(self):
        return f"{self.prenom} {self.nom}"