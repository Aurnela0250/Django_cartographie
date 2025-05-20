import json
import os
from datetime import datetime

import django

from apps.establishment.models import Establishment
from apps.establishment_type.models import EstablishmentType
from apps.formation.models import Formation
from apps.formation_authorization.models import FormationAuthorization
from apps.levels.models import Level
from apps.mentions.models import Mention
from apps.sector.models import Sector

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_cartographie.settings")
django.setup()

# Script de seed pour les établissements, formations et authorizations
# Inspiré de seed_regions_villes.py

# Charger le JSON depuis un fichier ou coller ici
DATA_JSON = """
{
  "items": [
    {
      "name": "ACEEM",
      "acronyme": "ACEEM",
      "address": " ",
      "formations": [
        {
          "intitule": "Informatique de Gestion",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "BUSINESS SCHOOL",
      "acronyme": "BUSINESS SCHOOL",
      "address": "Ankadivato",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2022-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupReS du 07 avril 2022"
          }
        },
        {
          "intitule": "Droit et Éthique des Affaires",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022-MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "UNIVERSITE SAINT VINCENT DE PAUL AKAMASOA Andralanitra",
      "acronyme": "",
      "address": "AKAMASOA Andralanitra",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31311/2023-MESupReS du 17 novembre 2023"
          }
        },
        {
          "intitule": "Pédagogie",
          "level_id": 1,
          "mention_id": 59,
          "authorization": {
            "date_debut": "2024-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31311/2023-MESupReS du 17 novembre 2024"
          }
        }
      ]
    },
    {
      "name": "AROVY UNIVERSITY",
      "acronyme": "AROVY UNIVERSITY",
      "address": "Ambohitantely",
      "formations": [
        {
          "intitule": "Electronique",
          "level_id": 1,
          "mention_id": 33,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31310/2023-MESupReS du 17 novembre 2023"
          }
        },
        {
          "intitule": "Electronique",
          "level_id": 3,
          "mention_id": 33,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31310/2023-MESupReS du 17 novembre 2023"
          }
        },
        {
          "intitule": "Ressources Minérales et Aménagement du Sous-sol",
          "level_id": 1,
          "mention_id": 28,
          "authorization": {
            "date_debut": "2024-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31310/2023-MESupReS du 17 novembre 2024"
          }
        },
        {
          "intitule": "Ressources Minérales et Aménagement du Sous-sol",
          "level_id": 3,
          "mention_id": 28,
          "authorization": {
            "date_debut": "2024-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31310/2023-MESupReS du 17 novembre 2024"
          }
        },
        {
          "intitule": "Energie Renouvelable",
          "level_id": 1,
          "mention_id": 37,
          "authorization": {
            "date_debut": "2025-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31310/2023-MESupReS du 17 novembre 2025"
          }
        },
        {
          "intitule": "Energie Renouvelable",
          "level_id": 3,
          "mention_id": 37,
          "authorization": {
            "date_debut": "2025-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31310/2023-MESupReS du 17 novembre 2025"
          }
        },
        {
          "intitule": "Economie et Ingénierie Financière",
          "level_id": 1,
          "mention_id": 4,
          "authorization": {
            "date_debut": "2026-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31310/2023-MESupReS du 17 novembre 2026"
          }
        },
        {
          "intitule": "Gestion des Entreprises et des Administrations",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2027-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31310/2023-MESupReS du 17 novembre 2027"
          }
        },
        {
          "intitule": "Gestion des Entreprises et des Administrations",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2027-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31310/2023-MESupReS du 17 novembre 2027"
          }
        },
        {
          "intitule": "Information et Communication",
          "level_id": 1,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2029-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31310/2023-MESupReS du 17 novembre 2029"
          }
        }
      ]
    },
    {
      "name": "ATHENEE SAINT JOSEPH ANTSIRABE",
      "acronyme": "A S J A",
      "address": "Antsirabe",
      "formations": [
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2011-06-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°19049/2011-MESupReS du 09 juin 2011"
          }
        },
        {
          "intitule": "Économie et Commerce",
          "level_id": 1,
          "mention_id": 4,
          "authorization": {
            "date_debut": "2012-06-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°19049/2011-MESupReS du 09 juin 2012"
          }
        },
        {
          "intitule": "Économie et Commerce",
          "level_id": 3,
          "mention_id": 4,
          "authorization": {
            "date_debut": "2013-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013-MESupReS du 23 avril 2013"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013-MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Sciences agronomiques",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2011-06-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°19048/2011-MESupReS du 09 juin 2011"
          }
        },
        {
          "intitule": "Sciences de la terre",
          "level_id": 1,
          "mention_id": 29,
          "authorization": {
            "date_debut": "2012-06-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°19048/2011-MESupReS du 09 juin 2012"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2013-06-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°19048/2011-MESupReS du 09 juin 2013"
          }
        },
        {
          "intitule": "Sciences agronomiques",
          "level_id": 3,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2013-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013-MESupReSdu 23 avril 2013"
          }
        },
        {
          "intitule": "Sciences de la terre",
          "level_id": 3,
          "mention_id": 29,
          "authorization": {
            "date_debut": "2014-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013-MESupReSdu 23 avril 2014"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2015-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013-MESupReSdu 23 avril 2015"
          }
        }
      ]
    },
    {
      "name": "BEATY UNIVERSITY",
      "acronyme": "BEATY UNIVERSITY",
      "address": "Toamasina",
      "formations": [
        {
          "intitule": "Sciences de Gestion",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "CENTRE D’ETUDES, DE L’INFORMATION ET SES TECHNOLOGIES, ORIENTE PROFESSIONNEL",
      "acronyme": "C E I T O P",
      "address": "Ambolokandrina",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2012-10-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°28879/2012-- MESupReS du 31 octobre 2012"
          }
        }
      ]
    },
    {
      "name": "CENTRE ECOLOGIQUE DE LIBANONA",
      "acronyme": "C E L",
      "address": "Ford-Dauphin",
      "formations": [
        {
          "intitule": "Gestion de l’Environnement au Service du Développement",
          "level_id": 1,
          "mention_id": 36,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014 rectifié par l’arrêté n°8015/2014-MESupReS du 29 janvier 2014"
          }
        }
      ]
    },
    {
      "name": "CONSEILS-ETUDES-REALISATION-FORMATION ARMI",
      "acronyme": "CERF ARMI",
      "address": "6 7Ha",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        }
      ]
    },
    {
      "name": "CENTRE DE FORMATION ET D’APPLICATION DU MACHINISME AGRICOLE ANTSIRABE",
      "acronyme": "C F A M A",
      "address": "Antsirabe",
      "formations": [
        {
          "intitule": "Machinisme Agricole",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35166/2014- MESupReS du 24 novembre 2014"
          }
        }
      ]
    },
    {
      "name": "CENTRE DE FORMATION DES RESSOURCES HUMAINES",
      "acronyme": "C F R H",
      "address": "Tsaralalàna",
      "formations": [
        {
          "intitule": "Gestion des Ressources Humaines",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2016-12-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°26308/2016- MESupReS du 09 Décembre 2016"
          }
        },
        {
          "intitule": "Master",
          "level_id": 3,
          "mention_id": null,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31002/2017- MESupReS du 13 Décembre 2017"
          }
        }
      ]
    },
    {
      "name": "CONSERVATOIRE NATIONAL DES ARTS ET METIERS",
      "acronyme": "C N A M",
      "address": "67 HA Maison des Produits",
      "formations": [
        {
          "intitule": "Management et Société",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2018-08-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°20995/2018- MESupReS du 30 août 2018"
          }
        },
        {
          "intitule": "Management et Société",
          "level_id": 3,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2018-08-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°20995/2018- MESupReS du 30 août 2018"
          }
        },
        {
          "intitule": "Sciences Industrielles et Technologies de l’Information",
          "level_id": 1,
          "mention_id": 39,
          "authorization": null
        },
        {
          "intitule": "Master",
          "level_id": 3,
          "mention_id": null,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTTTUT D’ADMINISTRATION DES ENTREPRISES",
      "acronyme": "COGEFE - FORMATION",
      "address": "Mahazoarivo - Antsirabe",
      "formations": [
        {
          "intitule": "Gestion d’Entreprise",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "CENTRE DE RESSOURCES, D’ASSISTANCE ET DE CONSEIL",
      "acronyme": "C R A C ETUDIANTS",
      "address": "Antsenakely - Antsirabe",
      "formations": [
        {
          "intitule": "Économie – Gestion",
          "level_id": 1,
          "mention_id": 4,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°34520/2023-MESupReS du 20 décembre 2023"
          }
        },
        {
          "intitule": "Économie – Gestion",
          "level_id": 3,
          "mention_id": 4,
          "authorization": null
        },
        {
          "intitule": "Droit",
          "level_id": 3,
          "mention_id": 2,
          "authorization": null
        }
      ]
    },
    {
      "name": "ENGINEERING AND BUSINESS MALAGASY",
      "acronyme": "E B M INSTITUTE",
      "address": "Antanetibe",
      "formations": [
        {
          "intitule": "Sciences de Gestion et Administration d’Entreprises",
          "level_id": 3,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Droit et Techniques des Affaires",
          "level_id": 3,
          "mention_id": 2,
          "authorization": null
        },
        {
          "intitule": "Gestion et Administration d’Entreprises",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023- MESupReS du 17 novembe 2023"
          }
        },
        {
          "intitule": "DTS et Licence",
          "level_id": 2,
          "mention_id": null,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°34520/2023-MESupRES du 20 décembre 2023"
          }
        },
        {
          "intitule": "DTS et Licence",
          "level_id": 1,
          "mention_id": null,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°34520/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "ECOLE DE COMPTABILITE ET D’ADMINISTRATION TARATRA",
      "acronyme": "E C A T TARATRA",
      "address": "Fianarantsoa",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        }
      ]
    },
    {
      "name": "ETABLISSEMENT D’ENSEIGNEMENT ET DE FORMATION PROFESSIONNELLE SUPERIEURE CONDORCET",
      "acronyme": "E E F P S CONDORCET",
      "address": "Faravohitra",
      "formations": [
        {
          "intitule": "Génie Civil",
          "level_id": 1,
          "mention_id": 31,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012-- MESupReSdu 5 décembre 2012"
          }
        },
        {
          "intitule": "Génie Civil et Industriel",
          "level_id": 3,
          "mention_id": 31,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        }
      ]
    },
    {
      "name": "ETABLISSEMENT PRIVE D’ENSEIGNEMENT SUPERIEUR LUMIERE",
      "acronyme": "E P E S L",
      "address": "Malaho",
      "formations": [
        {
          "intitule": "Gestion et Administration d’Entreprises",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014-MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Banque et Institutions de Micro finance",
          "level_id": 1,
          "mention_id": 22,
          "authorization": null
        },
        {
          "intitule": "Droit et Technique des Affaires",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        }
      ]
    },
    {
      "name": "ECOLE PROFESSIONNELLE SUPERIEURE AGRICOLE",
      "acronyme": "E P S A",
      "address": "Bevalala",
      "formations": [
        {
          "intitule": "Sciences Agronomiques",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2013-10-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31501/2013-MESupReS du 23 octobre 2013"
          }
        },
        {
          "intitule": "Sciences Agronomiques",
          "level_id": 3,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2022-05-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12568/2022-MESupReS du 05 mai 2022"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE DE BATIMENT ET TRAVAUX PUBLICS",
      "acronyme": "E S B T P B",
      "address": "Bevalala",
      "formations": [
        {
          "intitule": "Génie Civil",
          "level_id": 1,
          "mention_id": 31,
          "authorization": {
            "date_debut": "2013-10-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31501/2013-MESupReS du 23 octobre 2013"
          }
        }
      ]
    },
    {
      "name": "ESCAME",
      "acronyme": "ESCAME",
      "address": "Ambaranjana",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012-MESupRES du 5 décembre 2012"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014-MESupRES du 13 janvier 2014"
          }
        }
      ]
    },
    {
      "name": "E S C M BUSINESS SCHOOL",
      "acronyme": "E S C M BUSINESS SCHOOL",
      "address": "Ampasanimalo (Immeuble le Colisée)",
      "formations": [
        {
          "intitule": "Management des Affaires",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE DE COMMERCE ET TECHNIQUE",
      "acronyme": "E S C T",
      "address": "Analamahitsy",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Sciences Managériales",
          "level_id": 3,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°34520/2023-MESupReS du 20 décembre 2023"
          }
        },
        {
          "intitule": "Communication",
          "level_id": 1,
          "mention_id": 6,
          "authorization": null
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE DE DROIT",
      "acronyme": "E S D",
      "address": "Nanisana",
      "formations": [
        {
          "intitule": "Droit et Sciences Politiques",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2014-12-26",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°37440/2014-MESupReS du 26 décembre 2014"
          }
        },
        {
          "intitule": "Droit et Sciences Politiques",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2014-12-29",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°37564/2014-MESupReS du 29 décembre 2014"
          }
        },
        {
          "intitule": "Droit et Sciences Politiques",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE DE DEVELOPPEMENT ECONOMIQUE ET SOCIAL",
      "acronyme": "E S D E S",
      "address": "Ankadivato",
      "formations": [
        {
          "intitule": "Travail Social",
          "level_id": 1,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2016-12-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°26308/2016- MESupReS du 09 Décembre 2016"
          }
        },
        {
          "intitule": "Travail Social",
          "level_id": 3,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2018-12-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31122/2018- MESupReS du 11Décembre 2018"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023- MESupReS du 17 novembre 2023"
          }
        },
        {
          "intitule": "Économie",
          "level_id": 1,
          "mention_id": 4,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Agronomie",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Agronomie",
          "level_id": 3,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE D’INFORMATIQUE ET DE GESTION DES ENTREPRISES",
      "acronyme": "E S I G E",
      "address": "Mahajanga",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013- MESupReS du 23 avril 2013"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°36831/2013-MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Sciences de Gestion",
          "level_id": 3,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2022-05-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12560/2022-MESupReS du 05 mai 2022"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-06-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 21909/2014- MESupReS du 11 juin 2014"
          }
        },
        {
          "intitule": "Arts, Lettres et Sciences Humaines",
          "level_id": 1,
          "mention_id": 64,
          "authorization": {
            "date_debut": "2022-05-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12560/2022-MESupReS du 05 mai 2022"
          }
        },
        {
          "intitule": "Arts, Lettres et Sciences Humaines",
          "level_id": 3,
          "mention_id": 64,
          "authorization": {
            "date_debut": "2022-05-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12560/2022-MESupReS du 05 mai 2022"
          }
        },
        {
          "intitule": "Tourisme et Hôtellerie",
          "level_id": 1,
          "mention_id": 7,
          "authorization": null
        },
        {
          "intitule": "Droit et Sciences Politiques",
          "level_id": 1,
          "mention_id": 2,
          "authorization": null
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE DE MANAGEMENT ET D’INFORMATIQUE APPLIQUEE",
      "acronyme": "E S M I A",
      "address": "Mahamasina Atsimo",
      "formations": [
        {
          "intitule": "Gestion (Accrédité)",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Gestion (Accrédité)",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": null,
            "date_fin": null,
            "status": "REQUESTED",
            "arrete": null
          }
        }
      ]
    },
    {
      "name": "ETABLISSEMENT SUPERIEUR PROFESSIONNEL BUREAUTIQUE, INFORMATIQUE ET GESTION",
      "acronyme": "E S P BIG",
      "address": "Behoririka",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE PROFESSIONNELLE EN INFORMATIQUE ET COMMERCE",
      "acronyme": "E S P I C",
      "address": "67 ha N.O",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE SACRE- CŒUR D’ANTANIMENA",
      "acronyme": "E S S C A",
      "address": "Antanimena",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2012-10-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°28879/2012- MESupReS du 31 octobre 2012"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012- MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Sciences de Gestion (Management des Affaires)",
          "level_id": 3,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE SPECIALISEE EN DROIT",
      "acronyme": "E S S E D",
      "address": "Fort Duchesne - Ankatso",
      "formations": [
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE SAINT GABRIEL MAHAJANGA",
      "acronyme": "E S S G A M",
      "address": "Mahajanga",
      "formations": [
        {
          "intitule": "Commerce et Gestion",
          "level_id": 1,
          "mention_id": 21,
          "authorization": {
            "date_debut": "2013-10-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31501/2013- MESupReS du 23 octobre 2013"
          }
        },
        {
          "intitule": "Commerce et Gestion",
          "level_id": 3,
          "mention_id": 21,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017- MESupReS du 25 janvier 2017"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": null
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE SPECIALISEE DE VAKINAKARATRA",
      "acronyme": "E S S V A",
      "address": "Antsirabe",
      "formations": [
        {
          "intitule": "Électromécanique",
          "level_id": 1,
          "mention_id": 35,
          "authorization": {
            "date_debut": "2012-06-22",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12403/2012- MESupReS du 22 juin 2012"
          }
        },
        {
          "intitule": "Gestion Management",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Sciences et Techniques de l’Éducation",
          "level_id": 1,
          "mention_id": 60,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1071/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Communication et Journalisme",
          "level_id": 1,
          "mention_id": 6,
          "authorization": null
        },
        {
          "intitule": "Écotourisme et Hôtellerie",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2014-06-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 21909/2014- MESupReS du 11 juin 2014 Arrêté n°35052/2014- MESupReS du 24 novembre 2014"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE DE TECHNOLOGIE",
      "acronyme": "E S T",
      "address": "Antanimena (Immeuble SANTA)",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2012-08-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°21627/2012- MESupReS du 09 août 2012"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2013-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013- MESupReS du 23 avril 2013"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012- MESupReS du 05 décembre 2012"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012- MESupReS du 05 décembre 2012"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE DESTECHNOLOGIES DE L’INFORMATION",
      "acronyme": "E S T I",
      "address": "Antanimena",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2015-11-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33033/2015- MESupReS du 05 novembre 2015"
          }
        },
        {
          "intitule": "Ingénierie des Technologies de l’Information",
          "level_id": 3,
          "mention_id": 39,
          "authorization": {
            "date_debut": "2018-12-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31122/2018- MESupReS du 11 Décembre 2018"
          }
        }
      ]
    },
    {
      "name": "ENGINEERING SCHOOL OF TOURISM, INFORMATICS, INTERPRETERSHIP AND MANAGEMENT",
      "acronyme": "E S T I I M",
      "address": "67 Ha",
      "formations": [
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Droit et Sciences Politiques",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2014-06-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 21909/2014- MESupReS du 11 juin 2014"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-10-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31501/2013- MESupReS du 23 octobre 2013"
          }
        },
        {
          "intitule": "Interprétariat, Diplomatie et Sciences Politiques",
          "level_id": 1,
          "mention_id": 5,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        },
        {
          "intitule": "Administration, Management, Commerce, Marketing",
          "level_id": 1,
          "mention_id": 9,
          "authorization": null
        },
        {
          "intitule": "Tourisme, Hôtellerie et Environnement",
          "level_id": 3,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014-MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Tourisme, Hôtellerie et Environnement",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014-MESupRES du 13 janvier 2014 Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        },
        {
          "intitule": "Master",
          "level_id": 3,
          "mention_id": null,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014-MESupRES du 13 janvier 2014 Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014-MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-12-26",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°37440/2014-MESupReS du 26 décembre 2014"
          }
        },
        {
          "intitule": "Sciences de l’Interprétariat, de l’Information et de la Communication (SIIC)",
          "level_id": 1,
          "mention_id": 6,
          "authorization": null
        },
        {
          "intitule": "",
          "level_id": 1,
          "mention_id": null,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023-MESupReS du 17 novembre 2023"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE DE MANAGEMENT",
      "acronyme": "E S U M",
      "address": "Andavamamba",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Statistique",
          "level_id": 1,
          "mention_id": 24,
          "authorization": null
        },
        {
          "intitule": "Économie",
          "level_id": 1,
          "mention_id": 4,
          "authorization": null
        },
        {
          "intitule": "Communication",
          "level_id": 1,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023- MESupReS du 17 novembre 2023"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE YADA DE MADAGASCAR",
      "acronyme": "E S Y M",
      "address": "Alasora",
      "formations": [
        {
          "intitule": "Génie Civil",
          "level_id": 1,
          "mention_id": 31,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "EDUCATION IN TRAINING, EMPLOYMENT AND COMMUNICATION",
      "acronyme": "E T E C",
      "address": "Faravohitra",
      "formations": [
        {
          "intitule": "Bâtiment et Travaux Publics, Électromécanique",
          "level_id": 1,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2013-10-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31501/2013- MESupReS du 23 octobre 2013"
          }
        },
        {
          "intitule": "Bâtiment et Travaux Publics, Électromécanique",
          "level_id": 3,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Administration, Gestion, Finances, Informatique de Gestion",
          "level_id": 3,
          "mention_id": 9,
          "authorization": null
        },
        {
          "intitule": "Génie Logiciel, Réseaux",
          "level_id": 1,
          "mention_id": 56,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Génie Logiciel, Réseaux",
          "level_id": 3,
          "mention_id": 56,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        }
      ]
    },
    {
      "name": "ETABLISSEMENT TECHNIQUE DE FORMATION PROFESSIONNELLE SUPERIEURE",
      "acronyme": "E T F P S - R L G",
      "address": "Manjakaray",
      "formations": [
        {
          "intitule": "Génie Électrotechnique et Maintenance",
          "level_id": 1,
          "mention_id": 35,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": null
        },
        {
          "intitule": "Gestion et Management",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013 Arrêté n° 33033/2015- MESupReS du 05 novembre 2015"
          }
        }
      ]
    },
    {
      "name": "ETABLISSEMENT TECHNIQUE SUPERIEUR SAINT MICHEL",
      "acronyme": "E T S SAINT- MICHEL",
      "address": "Amparibe",
      "formations": [
        {
          "intitule": "Génie Mécanique et Informatique Industrielle",
          "level_id": 1,
          "mention_id": 54,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Génie Mécanique et Informatique Industrielle",
          "level_id": 3,
          "mention_id": 54,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Électromécanique et Automatisme Industriel",
          "level_id": 1,
          "mention_id": 58,
          "authorization": null
        },
        {
          "intitule": "Électromécanique et Automatisme Industriel",
          "level_id": 3,
          "mention_id": 58,
          "authorization": null
        },
        {
          "intitule": "Génie Industriel",
          "level_id": 1,
          "mention_id": 32,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1073/2014- MESupReS S du 13 janvier 2014"
          }
        },
        {
          "intitule": "Génie Industriel",
          "level_id": 3,
          "mention_id": 32,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1073/2014- MESupReS S du 13 janvier 2014"
          }
        }
      ]
    },
    {
      "name": "ESPACE UNIVERSITAIRE REGIONAL DE L’OCEAN INDIEN",
      "acronyme": "E U R O I",
      "address": "Ankadindramamy",
      "formations": [
        {
          "intitule": "Électronique et Télécommunication",
          "level_id": 1,
          "mention_id": 33,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Électronique et Télécommunication",
          "level_id": 3,
          "mention_id": 33,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014- MESupReS du 24 novembre 2014 (rnv : Arrêté n°3990/2022-MESupRes du 28 février 2022)"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE TOURISME ET DE L’HOTELLERIE",
      "acronyme": "EXCELLENCE",
      "address": "Antananarivo",
      "formations": [
        {
          "intitule": "Métiers du Tourisme et de l’Hôtellerie",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": null,
            "date_fin": null,
            "status": "REQUESTED",
            "arrete": null
          }
        }
      ]
    },
    {
      "name": "INGENIERIE ET MANAGEMENT DES ACTIONS DE DEVELOPPEMENT",
      "acronyme": "FFF MM – I M D",
      "address": "Fianarantsoa",
      "formations": [
        {
          "intitule": "Développement Local",
          "level_id": 1,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36.831/2013- MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Développement Local",
          "level_id": 3,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36.831/2013- MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Education et Développement Local",
          "level_id": 1,
          "mention_id": 60,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Education et Développement Local",
          "level_id": 3,
          "mention_id": 60,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "GRANDE ECOLE DE L’INNOVATION ET TECHNOLOGIE",
      "acronyme": "G E IT",
      "address": "Ambohibao Antehiroka",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": null,
            "date_fin": null,
            "status": "REQUESTED",
            "arrete": null
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": null,
            "date_fin": null,
            "status": "REQUESTED",
            "arrete": null
          }
        }
      ]
    },
    {
      "name": "GRAND SEMINAIRE SAINT PAUL APOTRE (Manantenasoa)",
      "acronyme": "G S S P A",
      "address": "Antsirabe",
      "formations": [
        {
          "intitule": "Philosophie",
          "level_id": 1,
          "mention_id": 12,
          "authorization": {
            "date_debut": "2015-11-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33033/2015- MESupReS du 05 novembre 2015"
          }
        }
      ]
    },
    {
      "name": "GATE UNIVERSITY AMBOHIDRATRIMO",
      "acronyme": "G U A",
      "address": "Ambohidratrimo",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013- MESupReS du 23 avril 2013"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Tourisme",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Agronomie",
          "level_id": 3,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Agronomie",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2014-12-26",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°37440/2014- MESupReS S du 26 décembre 2014"
          }
        }
      ]
    },
    {
      "name": "HAUTES ETUDES CHRETIENNES DE MANAGEMENT ET DE MATHEMATIQUES APPLIQUEES",
      "acronyme": "H E C M M A",
      "address": "Alarobia Amboniloha",
      "formations": [
        {
          "intitule": "Télécommunication Informatique et Électronique",
          "level_id": 1,
          "mention_id": 34,
          "authorization": {
            "date_debut": "2013-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013- MESupReS du 23 avril 2013 (rnv :Arrêté n°3992/2022-MESupRes du 28 février 2022)"
          }
        },
        {
          "intitule": "BTP et Aménagement du Territoire",
          "level_id": 3,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2015-11-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33033/2015- MESupReS du 05 novembre 2015"
          }
        },
        {
          "intitule": "Management et Sciences Économiques",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013 Arrêté n° 36831/2013- MESupReS du 30 décembre 2013 Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Management et Sciences Économiques",
          "level_id": 3,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013 Arrêté n° 36831/2013- MESupReS du 30 décembre 2013 Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "HAUTES ETUDES EN DROIT ET EN MANAGEMENT",
      "acronyme": "H E D M",
      "address": "Soanierana",
      "formations": [
        {
          "intitule": "Sciences de Gestion",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Sciences de Gestion",
          "level_id": 3,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Sciences juridiques",
          "level_id": 1,
          "mention_id": 17,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "HAUTE ECOLE D’INFORMATIQUE",
      "acronyme": "H E I",
      "address": "Ivandry",
      "formations": [
        {
          "intitule": "Mathématiques Appliquées et Informatique",
          "level_id": 1,
          "mention_id": 24,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023- MESupReS du 17 novembre 2023"
          }
        }
      ]
    },
    {
      "name": "INSTITUT CATHOLIQUE NOTRE DAME",
      "acronyme": "I C N D",
      "address": "Mahajanga",
      "formations": [
        {
          "intitule": "Études Françaises",
          "level_id": 1,
          "mention_id": 14,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023- MESupReS du 17 novembre 2023"
          }
        }
      ]
    },
    {
      "name": "INSTITUTION CHRETIENNE DE TSIENIMPARIHY, UNIE PAR LE SAUVEUR",
      "acronyme": "I C T U S",
      "address": "Ambalavao",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT D’ENSEIGNEMENT ET DE FORMATION PROFESSIONNELLE",
      "acronyme": "I E F P A A C E E M",
      "address": "Ambatomitsangana",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        }
      ]
    },
    {
      "name": "INSTITUT D’ETUDES POLITIQUES MADAGASCAR",
      "acronyme": "I E P",
      "address": "Ampandrana Ouest",
      "formations": [
        {
          "intitule": "Sciences Politiques",
          "level_id": 1,
          "mention_id": 5,
          "authorization": {
            "date_debut": "2013-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013- MESupReS du 23 avril 2013"
          }
        },
        {
          "intitule": "Sciences Politiques",
          "level_id": 3,
          "mention_id": 5,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        }
      ]
    },
    {
      "name": "INSTITUT D’ENSEIGNEMENT SUPERIEUR DE TECHNOLOGIE INFORMATIQUE ET DE MANAGEMENT D’ENTREPRISE",
      "acronyme": "I E S T I M E",
      "address": "Antaninandro",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Sciences de Gestion (FOAD)",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Sciences de Gestion (FOAD)",
          "level_id": 3,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Sciences de l’Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "INSTITUT D’ENSEIGNEMENT SUPERIEUR DE TECHNOLOGIE INFORMATIQUE ET DE MANAGEMENT D’ENTREPRISE",
      "acronyme": "I E S T I M E",
      "address": "Antsirabe",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Sciences de Gestion (FOAD)",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Sciences de Gestion (FOAD)",
          "level_id": 3,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION EN AGRONOMIE, GEMMOLOGIE, INDUSTRIALISATION ET PARAMED",
      "acronyme": "I F A G I et PARAMED",
      "address": "Andravoahangy ambony",
      "formations": [
        {
          "intitule": "Génie Civil",
          "level_id": 1,
          "mention_id": 31,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2014-12-26",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°37440/2014- MESupReS du 26 décembre 2014"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION PROFESSIONNELLE RAKETAMANGA",
      "acronyme": "I F P RAKETAMANGA",
      "address": "Antsirabe",
      "formations": [
        {
          "intitule": "Propriété Intellectuelle",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Muséologie",
          "level_id": 1,
          "mention_id": 15,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION DES ENSEIGNANTS A MADAGASCAR",
      "acronyme": "I F E M",
      "address": "Andrefan’Ambohijanahary",
      "formations": [
        {
          "intitule": "Pédagogie",
          "level_id": 1,
          "mention_id": 59,
          "authorization": {
            "date_debut": "2023-12-12",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°32897/2023- MESupReS du 12 décembre 2023"
          }
        },
        {
          "intitule": "Technologie de l’Education",
          "level_id": 3,
          "mention_id": 60,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION ET DES RECHERCHES PEDAGOGIQUES",
      "acronyme": "I F R P",
      "address": "Ambodin’Andohalo",
      "formations": [
        {
          "intitule": "Enseignements Littéraires",
          "level_id": 1,
          "mention_id": 61,
          "authorization": {
            "date_debut": "2015-11-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33033/2015- MESupReS du 05 novembre 2015"
          }
        },
        {
          "intitule": "Enseignements Scientifiques",
          "level_id": 1,
          "mention_id": 62,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION EN SAGE FEMME ET INFIRMIERE-INSTITUT EN TERTIAIRE ET MEDICAL",
      "acronyme": "I F S I - INTERMED",
      "address": "Andoharanofotsy",
      "formations": [
        {
          "intitule": "Gestion et Commerce International",
          "level_id": 2,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        },
        {
          "intitule": "Gestion et Commerce International",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION TECHNIQUE",
      "acronyme": "I F T",
      "address": "Antananarivo",
      "formations": [
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2012-06-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11118/2012- MESupReS du 05 juin 2012"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2014-12-26",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°37440/2014-MESupReS du 26 décembre 2014"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012- MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012- MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Bâtiment et Travaux Publics",
          "level_id": 1,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2012-08-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°21627/2012- MESupReS du 09 août 2012"
          }
        },
        {
          "intitule": "Bâtiment et Travaux Publics",
          "level_id": 3,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2012-08-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°21627/2012- MESupReS du 09 août 2012"
          }
        },
        {
          "intitule": "Information-Communication-Journalisme",
          "level_id": 1,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2012-10-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°28879/2012- MESupReS du 31 octobre 2012"
          }
        },
        {
          "intitule": "Information-Communication-Journalisme",
          "level_id": 3,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2012-10-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°28879/2012- MESupReS du 31 octobre 2012"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-06-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 21909/2014- MESupReS du 11 juin 2014"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Sciences de l’Environnement",
          "level_id": 1,
          "mention_id": 36,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013 Arrêté n°35052/2014- MESupReS du 24 novembre 2014 Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Sciences de l’Environnement",
          "level_id": 3,
          "mention_id": 36,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013 Arrêté n°35052/2014- MESupReS du 24 novembre 2014 Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Tourisme et culture",
          "level_id": 3,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013 Arrêté n°35052/2014- MESupReS du 24 novembre 2014 Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION TECHNIQUE",
      "acronyme": "I F T",
      "address": "Antsirabe",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014- MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Tourisme et Hôtellerie",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION TECHNIQUE",
      "acronyme": "I F T",
      "address": "Fianarantsoa",
      "formations": [
        {
          "intitule": "B T P",
          "level_id": 1,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014- MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Gestion Management",
          "level_id": 1,
          "mention_id": 3,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION TECHNIQUE",
      "acronyme": "I F T",
      "address": "Mahajanga",
      "formations": [
        {
          "intitule": "Sciences de l’Environnement",
          "level_id": 1,
          "mention_id": 36,
          "authorization": null
        },
        {
          "intitule": "Gestion Management",
          "level_id": 1,
          "mention_id": 3,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION TECHNIQUE",
      "acronyme": "I F T",
      "address": "Toamasina",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2015-11-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33033/2015- MESupReS du 05 novembre 2015"
          }
        },
        {
          "intitule": "BTP",
          "level_id": 1,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DE GEOGRAPHIE DE LA SOFIA",
      "acronyme": "I G S",
      "address": "Antsohihy",
      "formations": [
        {
          "intitule": "Géographie humaine",
          "level_id": 3,
          "mention_id": 66,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT INTERNATIONAL DE LEADERSHIP ET MANAGEMENT",
      "acronyme": "I I L M",
      "address": "Antananarivo",
      "formations": [
        {
          "intitule": "Leadership et Management",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 31307/2023- MESupReS du 17 novembre 2023"
          }
        }
      ]
    },
    {
      "name": "INSTITUT INTERNATIONAL DES SCIENCES SOCIALES",
      "acronyme": "I I S S",
      "address": "Tsiadana",
      "formations": [
        {
          "intitule": "Hygiène-Sécurité-Environnement et Technologie",
          "level_id": 1,
          "mention_id": 36,
          "authorization": {
            "date_debut": "2017-12-21",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 31483/2017- MESupReSdu 21 décembre 2017"
          }
        },
        {
          "intitule": "Hygiène-Sécurité-Environnement et Technologie",
          "level_id": 3,
          "mention_id": 36,
          "authorization": {
            "date_debut": "2017-12-21",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 31483/2017- MESupReSdu 21 décembre 2017"
          }
        },
        {
          "intitule": "Sciences Économiques",
          "level_id": 1,
          "mention_id": 18,
          "authorization": null
        },
        {
          "intitule": "Sciences Économiques",
          "level_id": 3,
          "mention_id": 18,
          "authorization": null
        },
        {
          "intitule": "Communication et Société",
          "level_id": 1,
          "mention_id": 6,
          "authorization": null
        },
        {
          "intitule": "Communication et Société",
          "level_id": 3,
          "mention_id": 6,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT DE LEADERSHIP CHRETIEN",
      "acronyme": "I L C",
      "address": "Antaninandro",
      "formations": [
        {
          "intitule": "Management/Gestion",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013"
          }
        }
      ]
    },
    {
      "name": "IMAGE APPLI",
      "acronyme": "IMAGE APPLI",
      "address": "Ankerana Ankadindramamy",
      "formations": [
        {
          "intitule": "Gestion Économie, management et Commerce Management",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DE MANAGEMENT DES ARTS ET METIERS",
      "acronyme": "I M G A M",
      "address": "Ivandry",
      "formations": [
        {
          "intitule": "Sciences Biologiques et environnementales",
          "level_id": 1,
          "mention_id": 27,
          "authorization": {
            "date_debut": "2012-08-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°21627/2012- MESupReS du 09 août 2012"
          }
        },
        {
          "intitule": "Administration",
          "level_id": 1,
          "mention_id": 9,
          "authorization": null
        },
        {
          "intitule": "Management d’Entreprise et Banque",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Management d’Entreprise et Banque",
          "level_id": 3,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2014-06-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 21909/2014- MESupReS du 11 juin 2014"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DE MANAGEMENT ET DES SCIENCES APPLIQUEES D’ANTSIRANANA",
      "acronyme": "I M S A A",
      "address": "Antsiranana",
      "formations": [
        {
          "intitule": "Management des Opérations Bancaires et Assurances",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31312/2023-MESupReS du 17 novembre 2023"
          }
        },
        {
          "intitule": "Management de Communication et Marketing",
          "level_id": 1,
          "mention_id": 8,
          "authorization": null
        },
        {
          "intitule": "Génie Mécanique",
          "level_id": 1,
          "mention_id": 54,
          "authorization": null
        },
        {
          "intitule": "Génie Mécanique",
          "level_id": 3,
          "mention_id": 54,
          "authorization": null
        },
        {
          "intitule": "Administration Economique et Sociale",
          "level_id": 3,
          "mention_id": 9,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34519/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "INSTITUTE OF MANAGEMENT AND TOURISM",
      "acronyme": "I M T",
      "address": "Antanimena",
      "formations": [
        {
          "intitule": "Hotel and Tourism Management",
          "level_id": 3,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Hotel and Tourism Management",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2014-06-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 21909/2014- MESupReS du 11 juin 2014"
          }
        },
        {
          "intitule": "Management and Business Studies",
          "level_id": 3,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2014-06-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 21909/2014- MESupReS du 11 juin 2014"
          }
        },
        {
          "intitule": "Management and Business Studies",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014-MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Management and Business Studies",
          "level_id": 3,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014-MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Building and Public Work",
          "level_id": 1,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        },
        {
          "intitule": "Building and Public Work",
          "level_id": 3,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DES ARTS ET DES TECHNOLOGIES AVANCEES",
      "acronyme": "I N A T A",
      "address": "Ankadivato",
      "formations": [
        {
          "intitule": "Informatique, Arts et Multimédia",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2015-02-06",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10769/2015-MESupReS du 6 février 2015"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION EN TOURISME",
      "acronyme": "INFOTOUR",
      "address": "Ankadivato",
      "formations": [
        {
          "intitule": "Tourisme et Hôtellerie",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DE FORMATION EN TOURISME",
      "acronyme": "INFOTOUR",
      "address": "Mahajanga",
      "formations": [
        {
          "intitule": "Tourisme et Hôtellerie",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR INDISPENSABLE AU DEVELOPPEMENT ROSSIGNOL",
      "acronyme": "INSIDE UNIVERSITY ROSSIGNOL",
      "address": "Ambondrona",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31003/2017-MESupReS du 13 décembre 2017"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023-MESupReS du 17 novembre 2023"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR PRIVE DES NOVATEURS DE MADAGASCAR",
      "acronyme": "INSPNMAD ANALAMANGA",
      "address": "Ambaranjana",
      "formations": [
        {
          "intitule": "Banque et Institutions des micros finances",
          "level_id": 3,
          "mention_id": 22,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Gestion et Administration d’Entreprises",
          "level_id": 3,
          "mention_id": 3,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR PRIVE DES NOVATEURS DE MADAGASCAR",
      "acronyme": "INSPNMAD MAHAJANGA",
      "address": "Mahajanga",
      "formations": [
        {
          "intitule": "Gestion et Administration d’Entreprises",
          "level_id": 2,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Gestion et Administration d’Entreprises",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Gestion et Administration d’Entreprises",
          "level_id": 3,
          "mention_id": 3,
          "authorization": null
        },
        {
          "intitule": "Marketing et Commerce International",
          "level_id": 1,
          "mention_id": 19,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "INSTITUTE OF TECHNICAL TECHNOLOGY, LIVING AND INTERDISCIPLINARY ARTS OF MADAGASCAR",
      "acronyme": "INTETLIAM",
      "address": "Andranovory",
      "formations": [
        {
          "intitule": "Bâtiment et Travaux Publics, Architecture",
          "level_id": 3,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        }
      ]
    },
    {
      "name": "INDIAN OCEAN ISLANDS UNIVERSITY",
      "acronyme": "I O I U",
      "address": "Andranonahoatra Itaosy",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34521/2023-MESupRES du 20 décembre 2023"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34521/2023-MESupRES du 20 décembre 2023"
          }
        },
        {
          "intitule": "Agronomie",
          "level_id": 1,
          "mention_id": 30,
          "authorization": null
        },
        {
          "intitule": "Agronomie",
          "level_id": 3,
          "mention_id": 30,
          "authorization": null
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": null
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": null
        }
      ]
    },
    {
      "name": "IVON-TOERAM-PAMPIANARANA AMBONY MOMBA NY EOKOMENISMA",
      "acronyme": "I P A E",
      "address": "Anjohy",
      "formations": [
        {
          "intitule": "Études œcuméniques",
          "level_id": 1,
          "mention_id": 67,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "INSTITUT PRIVE AL MOUSTAPHA",
      "acronyme": "I P A M",
      "address": "Ambohitrarahaba",
      "formations": [
        {
          "intitule": "Langue et Littérature Arabes",
          "level_id": 1,
          "mention_id": 14,
          "authorization": {
            "date_debut": "2014-01-29",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°8012/2014- MESupReS du 29 janvier 2014"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT PROFESSIONNEL SUPERIEUR EN AGRONOMIE ET EN TECHNOLOGIE DE TOMBOTSOA ANTSIRABE",
      "acronyme": "I P S A T T A",
      "address": "Antsirabe II",
      "formations": [
        {
          "intitule": "Sciences Agronomiques",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2015-11-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33033/2015- MESupReS du 05 novembre 2015"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR D’AMBATOMIRAHAVANY",
      "acronyme": "I S A",
      "address": "Ambatomirahavavy",
      "formations": [
        {
          "intitule": "Gestion et Création d’Entreprise",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT EN ADMINISTRATION D’ENTREPRISE « CABINET ATOMIC »",
      "acronyme": "I S A E",
      "address": "Ankatso",
      "formations": [
        {
          "intitule": "Management",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2014-06-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 21909/2014- MESupReS du 11 juin 2014"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DES AVENIRS PROFESSIONNELS",
      "acronyme": "I S A P",
      "address": "Ambohidrapeto Itaosy",
      "formations": [
        {
          "intitule": "Communication et Journalisme",
          "level_id": 1,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31003/2017-MESupReS du 13 décembre 2017"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": null
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR POUR L’AVENIR DES POLYTECHNICIENS ET DE LA SANTE PUBLIQUE",
      "acronyme": "I S A P S P",
      "address": "Ambanja",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Bâtiment et travaux Publics",
          "level_id": 1,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR ATOUT TOURISME MADAGASCAR",
      "acronyme": "I S - A T M",
      "address": "Ankorahotra",
      "formations": [
        {
          "intitule": "Hôtellerie /Tourisme",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31004/2017- MESupReS du 13 Décembre 2017"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE LA COMMUNICATION DES AFFAIRES ET DE MANAGEMENT",
      "acronyme": "I S C A M",
      "address": "Ankadifotsy",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2012-06-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11118/2012- MESupReS du 05 juin 2012"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-08-16",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°16049//2013- MESupReS du 16 août 2013"
          }
        },
        {
          "intitule": "Sciences de Gestion",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2022-07-21",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°19459/2022- MESupReS du 21 juillet 2022"
          }
        },
        {
          "intitule": "Sciences de Gestion",
          "level_id": 3,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2022-07-21",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°19459/2022- MESupReS du 21 juillet 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR CATHOLIQUE DU MENABE",
      "acronyme": "I S C A M E N",
      "address": "Morondava",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Métier de l’Enseignement et de l’Éducation Scientifique",
          "level_id": 1,
          "mention_id": 62,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2016-12-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°26308/2016 MESupReS du 09 Décembre 2016"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR POUR LE DEVELOPPEMENT DE L’ENTREPRENARIAT",
      "acronyme": "I S D E",
      "address": "67 Ha Sud",
      "formations": [
        {
          "intitule": "Administration et gestion d’Entreprise",
          "level_id": 2,
          "mention_id": 9,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Administration et gestion d’Entreprise",
          "level_id": 1,
          "mention_id": 9,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR POUR L’ENTREPRENEURIAT, LE COMMERCE ET LE MANAGEMENT",
      "acronyme": "I S E C O M",
      "address": "Ampasamadinika",
      "formations": [
        {
          "intitule": "Commerce International et Opérations Douanières",
          "level_id": 1,
          "mention_id": 21,
          "authorization": {
            "date_debut": "2016-12-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°26308/2016- MESupReS du 09 Décembre 2016"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR D’ENSEIGNEMENT TECHNOLOGIQUE ET DES SCIENCES",
      "acronyme": "I S E T S",
      "address": "Ambohidahy Ankadindramamy",
      "formations": [
        {
          "intitule": "Communication",
          "level_id": 1,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2016-12-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°26308/2016- MESupReS du 09 Décembre 2016"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31003/2017- MESupReS du 13 décembre 2017"
          }
        },
        {
          "intitule": "Génie Civil",
          "level_id": 1,
          "mention_id": 31,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE GENIE ELECTRONIQUE INFORMATIQUE",
      "acronyme": "I S G E I",
      "address": "Ampandrana Ouest",
      "formations": [
        {
          "intitule": "Ingénierie en Signaux, Images et Systèmes Associés",
          "level_id": 1,
          "mention_id": 40,
          "authorization": {
            "date_debut": "2012-06-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11118/2012- MESupReS du 05 juin 2012"
          }
        },
        {
          "intitule": "Ingénierie en Signaux, Images et Systèmes Associés",
          "level_id": 3,
          "mention_id": 40,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE GEOLOGIE DE L’INGENIEUR ET DE L’ENVIRONNEMENT DE MADAGASCAR",
      "acronyme": "I S G I E M",
      "address": "Ankadivato",
      "formations": [
        {
          "intitule": "Géologie de l’Ingénieur et de l’Environnement",
          "level_id": 1,
          "mention_id": 28,
          "authorization": {
            "date_debut": "2014-09-19",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°28716/2014-MESupReS du 19 septembre 2014"
          }
        },
        {
          "intitule": "Génie Civil",
          "level_id": 1,
          "mention_id": 31,
          "authorization": {
            "date_debut": "2014-09-19",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°28716/2014-MESupReS du 19 septembre 2014"
          }
        },
        {
          "intitule": "Génie géologique",
          "level_id": 3,
          "mention_id": 28,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35050/2014-MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Environnement et gestion durable Des ressources naturelles",
          "level_id": 3,
          "mention_id": 36,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE L’INNOVATION D’ANTSIRANANA",
      "acronyme": "I S I A",
      "address": "Antsiranana",
      "formations": [
        {
          "intitule": "Management et Commerce International",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR D’ELECTRONIQUE ET DE SYSTEME INFORMATIQUE",
      "acronyme": "I S – I E S I",
      "address": "Anjanahary",
      "formations": [
        {
          "intitule": "Informatique, Télécommunication et Électronique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014-MESupReS du 24 novembre 2014"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR D’INFORMATIQUE ET DE MANAGEMENT D’ENTREPRISE",
      "acronyme": "I S I M E",
      "address": "Betongolo",
      "formations": [
        {
          "intitule": "Gestion Informatique",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2016-12-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°26308/2016- MESupReS du 09 Décembre 2016"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014- MESupReS du 24 novembre 2014"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR EN INFORMATIQUE",
      "acronyme": "I S - I N F O",
      "address": "Ampasamadinika",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014 -MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014-MESupReS du 24 novembre 2014"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE L’INGENIERIE ET DES TECHNIQUES DE MANAGEMENT",
      "acronyme": "I S I T M",
      "address": "Ankatso",
      "formations": [
        {
          "intitule": "Génie Civil",
          "level_id": 1,
          "mention_id": 31,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DES METIERS DE MADAGASCAR",
      "acronyme": "I S 2 M",
      "address": "Ankaditapaka Ambohimitsimbina",
      "formations": [
        {
          "intitule": "Mathématiques Appliquées en informatique",
          "level_id": 1,
          "mention_id": 24,
          "authorization": {
            "date_debut": "2012-08-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°21627/2012- MESupReS du 09 août 2012"
          }
        },
        {
          "intitule": "Technologies et Méthodes Informatiques",
          "level_id": 1,
          "mention_id": 39,
          "authorization": null
        },
        {
          "intitule": "Économie – Management",
          "level_id": 3,
          "mention_id": 4,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Management et ingénierie économique",
          "level_id": 3,
          "mention_id": 8,
          "authorization": null
        },
        {
          "intitule": "Licence",
          "level_id": 1,
          "mention_id": null,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReSdu 23 mai 2013"
          }
        },
        {
          "intitule": "Master",
          "level_id": 3,
          "mention_id": null,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014- MESupReS du 24 novembre 2014"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR EN MANAGEMENT ET DU DEVELOPPEMENT D’ANTSIRANANA",
      "acronyme": "I S M A D A",
      "address": "Antsiranana",
      "formations": [
        {
          "intitule": "Management et Développement",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2018-12-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31122/2018- MESupReS du 11Décembre 2018"
          }
        },
        {
          "intitule": "Management et Développement",
          "level_id": 3,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2018-12-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31122/2018- MESupReS du 11Décembre 2018"
          }
        }
      ]
    },
    {
      "name": "INSTITUT UNIVERSITAIRE POLYTECHNIQUE DE MADAGASCAR",
      "acronyme": "I S M ADVANCEA",
      "address": "Ambohijatovo",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31003/2017- MESupReS du 13 décembre 2017"
          }
        },
        {
          "intitule": "Tourisme",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014- MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2015-02-06",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10769/2015- MESupReS du 6 février 2015"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2015-11-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33033/2015- MESupReS du 05 novembre 2015"
          }
        }
      ]
    },
    {
      "name": "INSTITUT DES SCIENCES MEDICALES, DE L’ADMINISTRATION ET DE LA TECHNOLOGIE",
      "acronyme": "I S M A T E C",
      "address": "Ankaditapaka",
      "formations": [
        {
          "intitule": "Sciences Managériales",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023- MESupReS du 17 novembre 2023 Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        },
        {
          "intitule": "Bâtiment et Travaux Publics",
          "level_id": 1,
          "mention_id": 38,
          "authorization": null
        },
        {
          "intitule": "Agronomie",
          "level_id": 1,
          "mention_id": 30,
          "authorization": null
        },
        {
          "intitule": "Communication",
          "level_id": 1,
          "mention_id": 6,
          "authorization": null
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR MONSEIGNEUR RAMAROSANDRATANA",
      "acronyme": "I S M R",
      "address": "Miarinarivo",
      "formations": [
        {
          "intitule": "Appui au Développement Local",
          "level_id": 1,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013 (rnv : Arrêté n°3992/2022- MESupReS du 28 février 2022)"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE MANAGEMENT ET DES SCIENCES TECHNOLOGIQUES",
      "acronyme": "I S M S T",
      "address": "Mahajanga",
      "formations": [
        {
          "intitule": "Gestion en Administration d’Entreprise",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2018-12-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31122/2018- MESupReS du 11Décembre 2018"
          }
        },
        {
          "intitule": "Droit et Sciences Politiques",
          "level_id": 1,
          "mention_id": 2,
          "authorization": null
        },
        {
          "intitule": "Droit des Affaires et Administration d’Entreprises",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Sciences de l’eau",
          "level_id": 2,
          "mention_id": 28,
          "authorization": {
            "date_debut": "2022-05-03",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12295/2022- MESupReS du 03 mai 2022"
          }
        },
        {
          "intitule": "Sciences de l’eau",
          "level_id": 1,
          "mention_id": 28,
          "authorization": {
            "date_debut": "2022-05-03",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12295/2022- MESupReS du 03 mai 2022"
          }
        },
        {
          "intitule": "Sciences de l’eau et de l’Environnement",
          "level_id": 3,
          "mention_id": 36,
          "authorization": null
        },
        {
          "intitule": "Ingénierie en Informatique",
          "level_id": 1,
          "mention_id": 56,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023- MESupReS du 17 novembre 2023"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE MANAGEMENT ET DE TECHNOLOGIE",
      "acronyme": "I S M T",
      "address": "Fianarantsoa",
      "formations": [
        {
          "intitule": "Technologie Informatique",
          "level_id": 1,
          "mention_id": 39,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR NUMERIQUE D’ANTANANARIVO",
      "acronyme": "I S N A",
      "address": "Antetezana Bongatsara",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2018-01-15",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°595/2018- MESupReS du 15 janvier 2018"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2018-12-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31122/2018- MESupReS du 11Décembre 2018"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR NORD MADAGASCAR",
      "acronyme": "I S N M",
      "address": "Antsiranana",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2014-12-26",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°37440/2014-MESupReS du 26 décembre 2014"
          }
        },
        {
          "intitule": "Génie Informatique",
          "level_id": 1,
          "mention_id": 56,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE PEDAGOGIE D’ANTANANARIVO Affilé à l’UCM",
      "acronyme": "I S P A",
      "address": "Antamponankatso",
      "formations": [
        {
          "intitule": "Mathématiques – Physique -Sciences de la Vie et de la Terre",
          "level_id": 1,
          "mention_id": 24,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012- MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Métier de l’enseignement et de l’éducation littéraire",
          "level_id": 1,
          "mention_id": 61,
          "authorization": null
        },
        {
          "intitule": "Formation des Formateurs des Enseignants en Secondaire Littéraire et Sciences Humaines",
          "level_id": 1,
          "mention_id": 63,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Formation des Formateurs des Enseignants en Secondaire Scientifiques",
          "level_id": 1,
          "mention_id": 63,
          "authorization": null
        },
        {
          "intitule": "Formation des Formateurs des Enseignants de l’Education de Base",
          "level_id": 3,
          "mention_id": 63,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34522/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR PRIVE AGRICOLE",
      "acronyme": "I S PAg",
      "address": "Ampandrianomby",
      "formations": [
        {
          "intitule": "Agronomie",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012- MESupReS du 5 décembre 2012"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR POLYTECHNIQUE DE MADAGASCAR",
      "acronyme": "I S P M",
      "address": "Ambatomaro Antsobolo",
      "formations": [
        {
          "intitule": "Biotechnologies",
          "level_id": 1,
          "mention_id": 27,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012- MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Biotechnologies",
          "level_id": 3,
          "mention_id": 27,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012- MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Génie Industriel",
          "level_id": 1,
          "mention_id": 32,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Génie Industriel",
          "level_id": 3,
          "mention_id": 32,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013- MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Génie Civil et Architecture",
          "level_id": 1,
          "mention_id": 31,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013 MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Génie Civil et Architecture",
          "level_id": 3,
          "mention_id": 31,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013 MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Informatique et télécommunication",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReSdu 23 mai 2013"
          }
        },
        {
          "intitule": "Informatique et télécommunication",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReSdu 23 mai 2013"
          }
        },
        {
          "intitule": "Droit et Technique des Affaires",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2014-11-04",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33213/2014- MESupReS du 04 novembre 2014 Arrêté n°33033/2015- MESupReS du 05 novembre 2015 Arrêté n°33213/2014-MESupReS du 04 novembre 2014 Arrêté n°37440/2014-MESupReS du 26 décembre 2014"
          }
        },
        {
          "intitule": "Droit et Technique des Affaires",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2014-11-04",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33213/2014- MESupReS du 04 novembre 2014 Arrêté n°33033/2015- MESupReS du 05 novembre 2015 Arrêté n°33213/2014-MESupReS du 04 novembre 2014 Arrêté n°37440/2014-MESupReS du 26 décembre 2014"
          }
        },
        {
          "intitule": "Technique du Tourisme",
          "level_id": 1,
          "mention_id": 7,
          "authorization": null
        },
        {
          "intitule": "Technique du Tourisme",
          "level_id": 3,
          "mention_id": 7,
          "authorization": null
        },
        {
          "intitule": "Technique de l’environnement et du Tourisme",
          "level_id": 1,
          "mention_id": 36,
          "authorization": null
        },
        {
          "intitule": "Technique de l’environnement et du Tourisme",
          "level_id": 3,
          "mention_id": 36,
          "authorization": null
        },
        {
          "intitule": "Environnement et Tourisme",
          "level_id": 1,
          "mention_id": 36,
          "authorization": null
        },
        {
          "intitule": "Environnement et Tourisme",
          "level_id": 3,
          "mention_id": 36,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR PRIVE MADAGASCAR DEVELOPPEMENT FORMATION",
      "acronyme": "IS P- M D F",
      "address": "Isoraka",
      "formations": [
        {
          "intitule": "Gestion et Commerce International",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR PROTESTANT PAUL MINAULT",
      "acronyme": "I S P P M",
      "address": "Ambohijatovo Atsimo",
      "formations": [
        {
          "intitule": "Sciences agronomiques",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2012-10-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°28879/2012- MESupReS du 31 octobre 2012"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR PRIVE DE LA REGION DIANA",
      "acronyme": "I S P R D",
      "address": "Antsiranana",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DES POLYTECHNICIENS DE LA REGION D’ITASY",
      "acronyme": "I S P R I",
      "address": "Analavory",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DES SCIENCES DE DEVELOPPEMENT",
      "acronyme": "I S S D",
      "address": "Fianarantsoa",
      "formations": [
        {
          "intitule": "Ingénierie Sociale",
          "level_id": 1,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Ingénierie Sociale",
          "level_id": 3,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        },
        {
          "intitule": "Management",
          "level_id": 3,
          "mention_id": 8,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR EN SCIENCES DE L’ENVIRONNEMENT ET DE GESTION",
      "acronyme": "I S S E G",
      "address": "Soanierana",
      "formations": [
        {
          "intitule": "Sciences de l’Environnement",
          "level_id": 1,
          "mention_id": 36,
          "authorization": {
            "date_debut": "2014-12-26",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°37440/2014-MESupReS du 26 décembre 2014"
          }
        },
        {
          "intitule": "Management et ses Applications",
          "level_id": 3,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR SPECIALISE EN INFORMATIQUE ET EN GESTION Infocentre de la Salle",
      "acronyme": "I S S I G",
      "address": "Soavimbahoaka",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014-MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": null
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR SAINT MICHEL ITAOSY",
      "acronyme": "I S S M I",
      "address": "Itaosy",
      "formations": [
        {
          "intitule": "Gestion managériale",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013-MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013-MESupeS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2016-12-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°26308/2016-MESupReS du 09 Décembre 2016"
          }
        },
        {
          "intitule": "Tourisme, Environnement et Hôtellerie",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014-MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Administration",
          "level_id": 3,
          "mention_id": 9,
          "authorization": null
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31003/2017-MESupReS du 13 décembre 2017 Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR SALESIEN DE PHILOSOPHIE SAINT THOMAS D’AQUIN",
      "acronyme": "I S S A P H I",
      "address": "Fianarantsoa",
      "formations": [
        {
          "intitule": "Philosophie",
          "level_id": 1,
          "mention_id": 12,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupRES du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE SPECIALISATION EN SCIENCES DE GESTION GROUPE EMIR Consulting",
      "acronyme": "I S S S G",
      "address": "Ankasina 67 HA",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupRES du 07 avril 2021"
          }
        },
        {
          "intitule": "Contrôle de Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31003/2017-MESupReS du 13 décembre 2017"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR PRIVE PROFESSIONNEL",
      "acronyme": "I S S U P",
      "address": "Behoririka",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2015-02-06",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10769/2015-MESupReS du 6 février 2015"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE TECHNOLOGIES",
      "acronyme": "I S T",
      "address": "Manakara",
      "formations": [
        {
          "intitule": "Métier de l’Eau et de l’Électricité",
          "level_id": 1,
          "mention_id": 55,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3996/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE TECHNOLOGIE INDUSTRIEL ET DE MANAGEMENT",
      "acronyme": "I S T I M E",
      "address": "Antsiranana",
      "formations": [
        {
          "intitule": "Génie Industriel et Maintenance",
          "level_id": 1,
          "mention_id": 32,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022- MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Gestion d’Entreprise et des Administrations",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2022-05-06",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12614/2022-MESupReS du 06 mai 2022"
          }
        },
        {
          "intitule": "Management des Entreprises",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2022-05-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12573/2022-MESupReS du 05 mai 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE TECHNOLOGIE REGIONAL DE FITOVINANY",
      "acronyme": "I S T R V",
      "address": "Manakara",
      "formations": [
        {
          "intitule": "Sciences Agronomiques et Halieutiques",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2015-02-06",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10770/2015- MESupReS du 6 février 2015"
          }
        },
        {
          "intitule": "Informatique systèmes, Télécommunication et Réseaux",
          "level_id": 1,
          "mention_id": 1,
          "authorization": null
        },
        {
          "intitule": "Électrotechnique, Électronique et Instrumentation Automatiques",
          "level_id": 2,
          "mention_id": 35,
          "authorization": {
            "date_debut": "2022-05-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12574/2022-MESupReS du 05 mai 2022"
          }
        },
        {
          "intitule": "Électrotechnique, Électronique et Instrumentation Automatiques",
          "level_id": 5,
          "mention_id": 35,
          "authorization": {
            "date_debut": "2022-05-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12574/2022-MESupReS du 05 mai 2022"
          }
        },
        {
          "intitule": "Électrotechnique, Électronique et Instrumentation Automatiques",
          "level_id": 1,
          "mention_id": 35,
          "authorization": {
            "date_debut": "2022-05-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°12574/2022-MESupReS du 05 mai 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT SUPERIEUR DE TRAVAIL SOCIAL",
      "acronyme": "I S T S",
      "address": "Iavoloha",
      "formations": [
        {
          "intitule": "Travail social (Accrédité)",
          "level_id": 1,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2012-08-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°21627/2012- MESupReS du 09 août 2012"
          }
        },
        {
          "intitule": "Travail social (Accrédité)",
          "level_id": 3,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2012-08-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°21627/2012- MESupReS du 09 août 2012"
          }
        }
      ]
    },
    {
      "name": "INSTITUT TECHNIQUE SUPERIEUR AGRICOLE",
      "acronyme": "I T S A",
      "address": "Antady Fianarantsoa",
      "formations": [
        {
          "intitule": "Sciences Agronomiques",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "INSTITUT TECHNIQUE SUPERIEUR FRANCOIS XAVIER",
      "acronyme": "I T S F X",
      "address": "Antady Fianarantsoa",
      "formations": [
        {
          "intitule": "Génie Industriel",
          "level_id": 1,
          "mention_id": 32,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "INFORMATION TECHNOLOGY UNIVERSITY",
      "acronyme": "I T U",
      "address": "Andoharanofotsy",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2012-06-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11118/2012- MESupReS du 05 juin 2012"
          }
        }
      ]
    },
    {
      "name": "INSTITUT UNIVERSITAIRE DE MADAGASCAR",
      "acronyme": "I U M",
      "address": "Isoraka",
      "formations": [
        {
          "intitule": "Gestion et Commerce",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35165/2014- MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Tourisme",
          "level_id": 1,
          "mention_id": 7,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3998/2022- MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "INSTITUT UNIVERSITAIRE PROFESSIONNEL EN ADMINISTRATION D’ENTREPRISE ET EN SCIENCES MARINES",
      "acronyme": "I U P - A E S M",
      "address": "NosyBe Hell –Ville",
      "formations": [
        {
          "intitule": "Administration d’Entreprise",
          "level_id": 2,
          "mention_id": 9,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Administration d’Entreprise",
          "level_id": 1,
          "mention_id": 9,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Sciences Marines et de l’Environnement",
          "level_id": 1,
          "mention_id": 36,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "JEANNE D’ARC UNIVERSITY (ne se trouve plus à cette adresse)",
      "acronyme": "J A U",
      "address": "Ampandrana Bel Air",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1073/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Sciences de la Gestion",
          "level_id": 1,
          "mention_id": 16,
          "authorization": null
        },
        {
          "intitule": "Communication",
          "level_id": 1,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31003/2017- MESupReS du 13 décembre 2017"
          }
        },
        {
          "intitule": "Communication",
          "level_id": 3,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31003/2017- MESupReS du 13 décembre 2017"
          }
        }
      ]
    },
    {
      "name": "LEADERSHIP MANAGEMENT BUSINESS UNIVERSITY",
      "acronyme": "L M B U",
      "address": "Ambatomaro",
      "formations": [
        {
          "intitule": "Sciences de la Gestion",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2015-11-03",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°32796/2015- MESupReS du 03 novembre 2015"
          }
        }
      ]
    },
    {
      "name": "LUTHERAN INSTITUTE OF MANAGEMENT AND ENTREPRENEURSHIP",
      "acronyme": "L I M E",
      "address": "Fianarantsoa",
      "formations": [
        {
          "intitule": "Management et Entreprenariat",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013- MESupReS du 23 mai 2013"
          }
        }
      ]
    },
    {
      "name": "MALAGASY INITIATIVE",
      "acronyme": "M I I",
      "address": "Toamasina",
      "formations": [
        {
          "intitule": "Transit et Douanes",
          "level_id": 1,
          "mention_id": 21,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34523/2023-MESupRES du 20 décembre 2023"
          }
        },
        {
          "intitule": "Management et Entreprenariat – Gestion des Ressources Humaines",
          "level_id": 1,
          "mention_id": 8,
          "authorization": null
        },
        {
          "intitule": "Langue Etrangère Appliquée",
          "level_id": 1,
          "mention_id": 14,
          "authorization": null
        },
        {
          "intitule": "Tourisme, Hôtellerie et Restauration",
          "level_id": 1,
          "mention_id": 7,
          "authorization": null
        }
      ]
    },
    {
      "name": "MAD’AID TRAINING CENTER",
      "acronyme": "M T C",
      "address": "Nanisana Iadiambola",
      "formations": [
        {
          "intitule": "Agronomie et Environnement",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2013-10-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31501/2013- MESupReS du 23 octobre 2013"
          }
        }
      ]
    },
    {
      "name": "MILLENIUM UNIVERSITY",
      "acronyme": "M U",
      "address": "Mahitsy",
      "formations": [
        {
          "intitule": "Sciences de la Gestion",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014- MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Sciences Juridiques",
          "level_id": 1,
          "mention_id": 17,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "MADAGASCAR UNIVERSITY OF SCIENCE AND TECHNOLOGY",
      "acronyme": "M UST UNIVERSITY",
      "address": "Ampefioha",
      "formations": [
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10276/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Économie",
          "level_id": 1,
          "mention_id": 4,
          "authorization": null
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": null
        }
      ]
    },
    {
      "name": "ONIVERSITE FJKM RAVELOJAONA",
      "acronyme": "O N I F R A",
      "address": "Ambatonakanga",
      "formations": [
        {
          "intitule": "Agronomie",
          "level_id": 1,
          "mention_id": 30,
          "authorization": {
            "date_debut": "2017-12-21",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31482/2017-MESupReS du 21 décembre 2017"
          }
        },
        {
          "intitule": "Génie Civil",
          "level_id": 1,
          "mention_id": 31,
          "authorization": null
        },
        {
          "intitule": "Sciences Appliquées et Environnement",
          "level_id": 1,
          "mention_id": 36,
          "authorization": {
            "date_debut": "2018-12-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31121/2018- MESupReS du 11Décembre 2018"
          }
        },
        {
          "intitule": "Sciences de la Communication et Multimédia",
          "level_id": 1,
          "mention_id": 6,
          "authorization": null
        },
        {
          "intitule": "Sciences de l’Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2019-04-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°8705/2019- MESupReS du 25 avril 2019"
          }
        },
        {
          "intitule": "Sciences de l’Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2019-04-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°8705/2019- MESupReS du 25 avril 2019"
          }
        },
        {
          "intitule": "Langue et lettres anglaises",
          "level_id": 1,
          "mention_id": 14,
          "authorization": null
        },
        {
          "intitule": "Tourisme",
          "level_id": 1,
          "mention_id": 7,
          "authorization": null
        },
        {
          "intitule": "Théologie",
          "level_id": 1,
          "mention_id": 67,
          "authorization": null
        },
        {
          "intitule": "Droit",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2017-12-21",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31482/2017-MESupReS du 21 décembre 2017"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2017-12-21",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31482/2017-MESupReS du 21 décembre 2017"
          }
        },
        {
          "intitule": "Licence",
          "level_id": 1,
          "mention_id": null,
          "authorization": {
            "date_debut": "2018-12-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31121/2018-MESupRES du 11Décembre 2018 Arrêté n°8705/2019-MESupRES du 25 avril 2019"
          }
        },
        {
          "intitule": "Master",
          "level_id": 3,
          "mention_id": null,
          "authorization": {
            "date_debut": "2018-12-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31121/2018-MESupRES du 11Décembre 2018 Arrêté n°8705/2019-MESupRES du 25 avril 2019"
          }
        }
      ]
    },
    {
      "name": "ONIVERSITE FJKM RAVELOJAONA",
      "acronyme": "O N I F R A",
      "address": "Ambatolampy",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023-MESupReSs du 17 novembre 2023"
          }
        }
      ]
    },
    {
      "name": "ONIVERSITE FJKM RAVELOJAONA",
      "acronyme": "O N I F R A",
      "address": "Arivonimamo",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "ONIVERSITE FJKM RAVELOJAONA",
      "acronyme": "O N I F R A",
      "address": "Moramanga",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupRES du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "ONIVERSITE FJKM RAVELOJAONA",
      "acronyme": "O N I F R A",
      "address": "Mahajanga",
      "formations": [
        {
          "intitule": "Sciences de Gestion",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "ONIVERSITE FJKM RAVELOJAONA",
      "acronyme": "O N I F R A",
      "address": "Toamasina",
      "formations": [
        {
          "intitule": "Sciences de Gestion",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 34520/2023-MESupRES du 20 décembre 2023"
          }
        }
      ]
    },
    {
      "name": "PHILOSOPHAT SAINT PAUL",
      "acronyme": "P S P",
      "address": "Ambanidia",
      "formations": [
        {
          "intitule": "Philosophie",
          "level_id": 1,
          "mention_id": 12,
          "authorization": {
            "date_debut": "2013-10-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31501/2013-MESupReS du 23 octobre 2013"
          }
        }
      ]
    },
    {
      "name": "SEKOLY AMBONY LOTERANA MOMBA NY TEOLOJIA",
      "acronyme": "S A L T",
      "address": "Fianarantsoa",
      "formations": [
        {
          "intitule": "Théologie",
          "level_id": 1,
          "mention_id": 67,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°36831/2013- MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Théologie",
          "level_id": 3,
          "mention_id": 67,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°36831/2013- MESupReS du 30 décembre 2013"
          }
        }
      ]
    },
    {
      "name": "ECOLE SUPERIEURE DE L’INFORMATION ET DE LA COMMUNICATION",
      "acronyme": "SAMIS - E S I C",
      "address": "Amparibe",
      "formations": [
        {
          "intitule": "Sciences de l’Information et Communication",
          "level_id": 1,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2013-10-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31501/2013-MESupReS du 23 octobre 2013"
          }
        },
        {
          "intitule": "Information et Communication",
          "level_id": 3,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36831/2013- MESupReS du 30 décembre 2013"
          }
        }
      ]
    },
    {
      "name": "ONG - UNIVERSITE POUR TOUS",
      "acronyme": "TANA PREMIER",
      "address": "Ambondrona",
      "formations": [
        {
          "intitule": "droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        }
      ]
    },
    {
      "name": "INSTITUT TOP INFO",
      "acronyme": "T O P I N F O",
      "address": "Anjanahary",
      "formations": [
        {
          "intitule": "Gestion et Informatique",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2016-12-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°26308/2016- MESupReS du 09 Décembre 2016"
          }
        }
      ]
    },
    {
      "name": "TECHNOLOGY SPECIALISTS INFORMATIC",
      "acronyme": "T S I",
      "address": "Ambatomaro",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2014-11-24",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°35052/2014-MESupReS du 24 novembre 2014"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2015-06-22",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°18373/2015-MESupReS du 22 juin 2015"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": null
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": null
        },
        {
          "intitule": "Agronomie",
          "level_id": 1,
          "mention_id": 30,
          "authorization": null
        },
        {
          "intitule": "Agronomie",
          "level_id": 3,
          "mention_id": 30,
          "authorization": null
        }
      ]
    },
    {
      "name": "UNIVERSITE ACEEM - MADAGASCAR BUSINESS SCHOOL -",
      "acronyme": "UNIVERSITE ACEEM",
      "address": "Manakambahiny",
      "formations": [
        {
          "intitule": "Informatique – Électronique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2012-06-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11118/2012- MESupReS du 05 juin 2012"
          }
        },
        {
          "intitule": "Technique médicale",
          "level_id": 1,
          "mention_id": 41,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012- MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Droit et Sciences politiques",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013-MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2014-12-29",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°37564/2014-MESupReS du 29 décembre 2014"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013-MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2014-06-11",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 21909/2014- MESupReS du 11 juin 2014"
          }
        },
        {
          "intitule": "Sciences de Gestion",
          "level_id": 3,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2014-11-04",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33213/2014-MESupReS du 04 novembre 2014"
          }
        },
        {
          "intitule": "Sciences de la Communication",
          "level_id": 3,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2013-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013- MESupReS du 23 avril 2013"
          }
        },
        {
          "intitule": "Sciences de la Communication",
          "level_id": 1,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2014-11-04",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33213/2014-MESupReS du 04 novembre 2014"
          }
        },
        {
          "intitule": "Sciences Économiques et Études de Développement",
          "level_id": 1,
          "mention_id": 18,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Relation Internationale et Diplomatie",
          "level_id": 1,
          "mention_id": 5,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023- MESupReS du 17 novembre 2023"
          }
        },
        {
          "intitule": "Management des Affaires",
          "level_id": 1,
          "mention_id": 8,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3997/2022-MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "UNIVERSITE ASCOM",
      "acronyme": "UNIVERSITE ASCOM",
      "address": "Ambodifilao (siège)",
      "formations": [
        {
          "intitule": "Sciences de Gestion",
          "level_id": 1,
          "mention_id": 16,
          "authorization": {
            "date_debut": "2015-11-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°33033/2015- MESupReS du 05 novembre 2015"
          }
        }
      ]
    },
    {
      "name": "UNIVERSITE ADVENTISTE ZÜRCHER",
      "acronyme": "U A Z",
      "address": "Sambaina Antsirabe",
      "formations": [
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2012-06-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11118/2012- MESupReS du 05 juin 2012"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 3,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021- MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Communication",
          "level_id": 3,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3392/2022-MESupReS du 28 février 2022"
          }
        },
        {
          "intitule": "Études en Théologie",
          "level_id": 1,
          "mention_id": 67,
          "authorization": null
        },
        {
          "intitule": "Études en Théologie",
          "level_id": 3,
          "mention_id": 67,
          "authorization": null
        },
        {
          "intitule": "Études Anglophones",
          "level_id": 1,
          "mention_id": 14,
          "authorization": null
        },
        {
          "intitule": "Études Anglophones",
          "level_id": 3,
          "mention_id": 14,
          "authorization": null
        },
        {
          "intitule": "Communication",
          "level_id": 1,
          "mention_id": 6,
          "authorization": null
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": null
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": null
        },
        {
          "intitule": "Droit",
          "level_id": 3,
          "mention_id": 2,
          "authorization": null
        }
      ]
    },
    {
      "name": "UNIVERSITE CATHOLIQUE DE MADAGASCAR - INSTITUT D’ANTHROPOLOGIE ET D’ECOLOGIE -",
      "acronyme": "U C M",
      "address": "Ambatoroka",
      "formations": [
        {
          "intitule": "Philosophie",
          "level_id": 1,
          "mention_id": 12,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31172/2012-MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Psychologie",
          "level_id": 3,
          "mention_id": 13,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 36.831/2013-MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Philosophie",
          "level_id": 1,
          "mention_id": 12,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013-MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Droit-Économie",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 31172/2012-MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Droit-Économie",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 31172/2012-MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2013-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013-MESupReS du 23 avril 2013"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 3,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2013-04-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°9188/2013-MESupReS du 23 avril 2013"
          }
        },
        {
          "intitule": "Économie et Gestion",
          "level_id": 1,
          "mention_id": 4,
          "authorization": {
            "date_debut": "2014-01-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1072/2014-MESupReS du 13 janvier 2014"
          }
        },
        {
          "intitule": "Sciences Sociales Appliquées au Développement",
          "level_id": 3,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2012-12-05",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n° 31172/2012-MESupReS du 5 décembre 2012"
          }
        },
        {
          "intitule": "Sciences Sociales Appliquées au Développement",
          "level_id": 1,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013-MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Sciences Sociales Appliquées au Développement",
          "level_id": 3,
          "mention_id": 15,
          "authorization": {
            "date_debut": "2013-05-23",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°11566/2013-MESupReS du 23 mai 2013"
          }
        },
        {
          "intitule": "Théologie",
          "level_id": 1,
          "mention_id": 67,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Théologie",
          "level_id": 3,
          "mention_id": 67,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 3,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Economie",
          "level_id": 3,
          "mention_id": 4,
          "authorization": {
            "date_debut": "2023-12-20",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°34524/2023- MESupReS du 20 décembre 2023"
          }
        },
        {
          "intitule": "Sciences Politiques",
          "level_id": 3,
          "mention_id": 5,
          "authorization": {
            "date_debut": "2018-03-06",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°5176/2018-MESupReS du 06 mars 2018"
          }
        },
        {
          "intitule": "Anthropologie et Écologie",
          "level_id": 3,
          "mention_id": 11,
          "authorization": null
        }
      ]
    },
    {
      "name": "UNIVERSITE DES MEDIAS, DE L’AUDIOVISUEL ET DE LA TECHNOLOGIE",
      "acronyme": "U E-MEDIA",
      "address": "Tsiadana Ampasanimalo",
      "formations": [
        {
          "intitule": "Marketing Publicité et Journalisme",
          "level_id": 1,
          "mention_id": 19,
          "authorization": {
            "date_debut": "2018-11-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°29.810/2018-MESupReS du 30 novembre 2018"
          }
        },
        {
          "intitule": "Marketing Publicité et Journalisme",
          "level_id": 3,
          "mention_id": 19,
          "authorization": {
            "date_debut": "2018-11-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°29.810/2018-MESupReS du 30 novembre 2018"
          }
        },
        {
          "intitule": "Audiovisuel et Cinématographie",
          "level_id": 1,
          "mention_id": 6,
          "authorization": null
        },
        {
          "intitule": "Communication Audiovisuelle et Numérique",
          "level_id": 1,
          "mention_id": 6,
          "authorization": null
        },
        {
          "intitule": "Informatique et Télécommunication",
          "level_id": 1,
          "mention_id": 1,
          "authorization": null
        },
        {
          "intitule": "Informatique et Électronique Embarquées",
          "level_id": 1,
          "mention_id": 1,
          "authorization": null
        },
        {
          "intitule": "Informatique et Électronique Embarquées",
          "level_id": 3,
          "mention_id": 1,
          "authorization": null
        }
      ]
    },
    {
      "name": "UNIVERSITÉ GENIUS SYSTEM INFORMATICS",
      "acronyme": "U - G S I",
      "address": "Antaninarenina",
      "formations": [
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013-MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2013-01-31",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1949/2013-MESupReS du 31 janvier 2013"
          }
        },
        {
          "intitule": "B TP",
          "level_id": 1,
          "mention_id": 38,
          "authorization": {
            "date_debut": "2013-12-30",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°36831/2013-MESupReS du 30 décembre 2013"
          }
        },
        {
          "intitule": "Communication journalisme et communication multimédia",
          "level_id": 1,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2014-12-29",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°37564/2014-MESupReS du 29 décembre 2014"
          }
        }
      ]
    },
    {
      "name": "UNIVERS INFORMATIQUE",
      "acronyme": "UNIVERS INFORMATIQUE",
      "address": "Andravoahangy",
      "formations": [
        {
          "intitule": "Gestion et Informatique",
          "level_id": 1,
          "mention_id": 3,
          "authorization": {
            "date_debut": "2016-12-09",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°26308/2016-MESupReS du 09 Décembre 2016"
          }
        }
      ]
    },
    {
      "name": "UNIVERSITE INTERNATIONALE DE MADAGASCAR",
      "acronyme": "U I M",
      "address": "Antetezanafovoany",
      "formations": [
        {
          "intitule": "Commerce",
          "level_id": 1,
          "mention_id": 21,
          "authorization": {
            "date_debut": "2017-12-13",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31003/2017-MESupReS du 13 décembre 2017"
          }
        },
        {
          "intitule": "Gestion",
          "level_id": 1,
          "mention_id": 3,
          "authorization": null
        },
        {
          "intitule": "Économie",
          "level_id": 1,
          "mention_id": 4,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Économie",
          "level_id": 3,
          "mention_id": 4,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Droit",
          "level_id": 1,
          "mention_id": 2,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3392/2022-MESupReS du 28 février 2022"
          }
        }
      ]
    },
    {
      "name": "UNIVERSITE OUEST D’IARIVO",
      "acronyme": "U O I",
      "address": "Ambohitrimanjaka",
      "formations": [
        {
          "intitule": "Science de l’Éducation Thérapeutique",
          "level_id": 1,
          "mention_id": 60,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        },
        {
          "intitule": "Informatique",
          "level_id": 1,
          "mention_id": 1,
          "authorization": null
        },
        {
          "intitule": "Ingénierie Informatique",
          "level_id": 1,
          "mention_id": 56,
          "authorization": {
            "date_debut": "2021-04-07",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°10275/2021-MESupReS du 07 avril 2021"
          }
        },
        {
          "intitule": "Licence",
          "level_id": 1,
          "mention_id": null,
          "authorization": {
            "date_debut": "2023-11-17",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°31309/2023-MESupReS du 17 novembre 2023"
          }
        }
      ]
    },
    {
      "name": "UNIVERSITE PRIVEE ALPHA SCHOOL",
      "acronyme": "U P ALPHA SCHOOL",
      "address": "Itaosy",
      "formations": [
        {
          "intitule": "Communication",
          "level_id": 1,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2017-01-25",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°1591/2017-MESupReS du 25 janvier 2017"
          }
        },
        {
          "intitule": "Communication",
          "level_id": 3,
          "mention_id": 6,
          "authorization": {
            "date_debut": "2022-02-28",
            "date_fin": null,
            "status": "VALIDATED",
            "arrete": "Arrêté n°3992/2022-MESupReS du 28 février 2022"
          }
        }
      ]
    }
  ]
}
"""

data = json.loads(DATA_JSON)

# À adapter selon votre logique métier
DEFAULT_SECTOR_NAME = "Général"
DEFAULT_ESTABLISHMENT_TYPE = "Privé"
DEFAULT_LEVEL_DURATION = 28  # Par défaut, durée d'une formation


def get_or_create_sector():
    sector, _ = Sector.objects.get_or_create(name=DEFAULT_SECTOR_NAME, city_id=1)
    return sector


def get_or_create_establishment_type():
    etype, _ = EstablishmentType.objects.get_or_create(name=DEFAULT_ESTABLISHMENT_TYPE)
    return etype


def get_level(level_id):
    try:
        return Level.objects.get(id=level_id)
    except Level.DoesNotExist:
        return None


def get_mention(mention_id):
    if mention_id is None:
        return None
    try:
        return Mention.objects.get(id=mention_id)
    except Mention.DoesNotExist:
        return None


def create_authorization(auth):
    if not auth:
        return None
    return FormationAuthorization.objects.create(
        date_debut=auth["date_debut"] or datetime.now().date(),
        date_fin=auth["date_fin"],
        status=auth["status"],
        arrete=auth["arrete"] or "",
    )


sector = get_or_create_sector()
est_type = get_or_create_establishment_type()

for item in data["items"]:
    est, _ = Establishment.objects.get_or_create(
        name=item["name"],
        defaults={
            "acronyme": item.get("acronyme", ""),
            "address": item.get("address", ""),
            "sector": sector,
            "establishment_type": est_type,
        },
    )
    for f in item["formations"]:
        level = get_level(f["level_id"])
        mention = get_mention(f["mention_id"])
        auth = (
            create_authorization(f["authorization"]) if f.get("authorization") else None
        )
        Formation.objects.get_or_create(
            intitule=f["intitule"],
            establishment=est,
            defaults={
                "level": level,
                "mention": mention,
                "duration": DEFAULT_LEVEL_DURATION,
                "authorization": auth,
            },
        )
