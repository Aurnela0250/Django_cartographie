# Ce script suppose que Django est déjà configuré (settings chargés)
import os

import django

from apps.city.models import City
from apps.region.models import Region

# Adapter ce chemin si besoin
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_cartographie.settings")
django.setup()


data = {
    "provinces": [
        {
            "nom": "Antananarivo",
            "chef_lieu": "Antananarivo",
            "regions": [
                {
                    "nom": "Itasy",
                    "villes": ["Miarinarivo", "Soavinandriana", "Arivonimamo"],
                },
                {
                    "nom": "Analamanga",
                    "villes": [
                        "Antananarivo",
                        "Ambohidratrimo",
                        "Anjozorobe",
                        "Manjakandriana",
                    ],
                },
                {
                    "nom": "Vakinankaratra",
                    "villes": ["Antsirabe", "Betafo", "Faratsiho", "Antanifotsy"],
                },
                {
                    "nom": "Bongolava",
                    "villes": ["Tsiroanomandidy", "Fenoarivo", "Fenoarivobe"],
                },
            ],
        },
        {
            "nom": "Antsiranana",
            "chef_lieu": "Antsiranana",
            "regions": [
                {
                    "nom": "Diana",
                    "villes": ["Antsiranana", "Ambilobe", "Nosy Be", "Ambanja"],
                },
                {
                    "nom": "Sava",
                    "villes": ["Sambava", "Antalaha", "Andapa", "Vohemar"],
                },
            ],
        },
        {
            "nom": "Fianarantsoa",
            "chef_lieu": "Fianarantsoa",
            "regions": [
                {
                    "nom": "Amoron'i Mania",
                    "villes": ["Ambositra", "Fandriana", "Manandriana"],
                },
                {
                    "nom": "Haute Matsiatra",
                    "villes": ["Fianarantsoa", "Ambalavao", "Ambohimahasoa"],
                },
                {
                    "nom": "Vatovavy-Fitovinany",
                    "villes": ["Manakara", "Ifanadiana", "Nosy Varika"],
                },
                {
                    "nom": "Atsimo-Atsinanana",
                    "villes": ["Farafangana", "Vangaindrano", "Vondrozo"],
                },
                {"nom": "Ihorombe", "villes": ["Ihosy", "Ivohibe", "Iakora"]},
            ],
        },
        {
            "nom": "Mahajanga",
            "chef_lieu": "Majunga",
            "regions": [
                {
                    "nom": "Sofia",
                    "villes": ["Antsohihy", "Bealanana", "Mandritsara"],
                },
                {"nom": "Boeny", "villes": ["Mahajanga", "Marovoay", "Mitsinjo"]},
                {
                    "nom": "Betsiboka",
                    "villes": ["Maevatanana", "Tsaratanana", "Kandreho"],
                },
                {
                    "nom": "Melaky",
                    "villes": ["Maintirano", "Morafenobe", "Besalampy"],
                },
            ],
        },
        {
            "nom": "Toamasina",
            "chef_lieu": "Toamasina",
            "regions": [
                {
                    "nom": "Alaotra-Mangoro",
                    "villes": ["Ambatondrazaka", "Moramanga", "Andilamena"],
                },
                {
                    "nom": "Atsinanana",
                    "villes": ["Toamasina", "Vatomandry", "Brickaville"],
                },
                {
                    "nom": "Analanjirofo",
                    "villes": [
                        "Fenoarivo Atsinanana",
                        "Mananara",
                        "Soanierana Ivongo",
                    ],
                },
            ],
        },
        {
            "nom": "Toliara",
            "chef_lieu": "Toliara",
            "regions": [
                {"nom": "Menabe", "villes": ["Morondava", "Mahabo", "Miandrivazo"]},
                {
                    "nom": "Atsimo-Andrefana",
                    "villes": ["Toliara", "Betioky", "Ampanihy"],
                },
                {"nom": "Androy", "villes": ["Ambovombe", "Tsiombe", "Beloha"]},
                {"nom": "Anosy", "villes": ["Tolagnaro", "Amboasary", "Betroka"]},
            ],
        },
    ]
}

for province in data["provinces"]:
    for region_data in province["regions"]:
        region_name = region_data["nom"]
        region, created = Region.objects.get_or_create(name=region_name)
        print(f"{'Créée' if created else 'Déjà existante'} région : {region_name}")

        for ville_name in region_data["villes"]:
            city, created = City.objects.get_or_create(name=ville_name, region=region)
            print(
                f"    {'Créée' if created else 'Déjà existante'} ville : {ville_name}"
            )
