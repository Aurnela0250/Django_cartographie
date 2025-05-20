Il y'a plusieurs utilisateurs :

- `SuperAdmin`
- `AdminSecteur`
- `AdminEtab`
- `SimpleUser`

# Tables

Se referer sur le mcd sur la photo

- `typeEtablissement` : e.g (Université, Centre de Formation, Grande Ecole, Institut)
- `domain` : e.g (Informatique, Agriculture, Communication, Management, etc...)
- `formation` : formation proposé par les établissements
- `autorisation` : e.g (accréditation, habilitation, agrée, etc...)

# Uses cases

## Permission et fonctionnalitées des utilisateurs

- `SuperAdmin` :
  - Crée les login de `AdminSecteur`
  - CRUD `domain`
  - CRUD `accréditation`
  - CRUD `secteur`
  - CRUD `region`
  - CRUD `typeEtablissement`
  - accèes à tous les fonctionnalité
- `AdminSecteur` :
  - crée login de `AdminEtablissement`
  - relie `etablissement` à son `autorisation`
  - valider les données de l'`etablissement` et `statistique` inscrit par l'`AdminEtablissement`.
  - accès à toute la liste des `établissement` de son secteur
  - Supprimer `etablissement`
- `AdminEtablissement`
  - CRU `etablissement`
  - CRUD `statistique`

## Fonctionalité de l'application

- Donnée statistiques pour chaque domaine :
  - Global :
    - Afficher le taux d'inscription des par `domain` et `année`.
    - Chatbot d'information pour se renseigner sur les universités
  - Par `etablissement` :
    - Afficher les statistiques de l'`etablissement` pour chaque.
    - Afficher les liste de tous les établissements
