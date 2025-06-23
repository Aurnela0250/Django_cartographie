#!/usr/bin/env python3
"""
Script de seed pour les régions et villes de Madagascar
"""
import asyncio
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tortoise import Tortoise

from apps.tortoise.city.models import City
from apps.tortoise.region.models import Region
from config.settings import TORTOISE_ORM

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


async def seed_regions_and_cities():
    """Seed les régions et villes dans la base de données"""
    print("🌱 Démarrage du seeding des régions et villes...")

    # Initialiser Tortoise ORM
    await Tortoise.init(config=TORTOISE_ORM)

    try:
        # Compter les éléments existants
        existing_regions = await Region.all().count()
        existing_cities = await City.all().count()
        print(f"📊 Régions existantes: {existing_regions}")
        print(f"📊 Villes existantes: {existing_cities}")

        regions_created = 0
        regions_existing = 0
        cities_created = 0
        cities_existing = 0

        for province in data["provinces"]:
            print(f"\n🏛️  Province: {province['nom']}")

            for region_data in province["regions"]:
                region_name = region_data["nom"]

                # Vérifier si la région existe déjà
                existing_region = await Region.filter(name=region_name).first()

                if existing_region:
                    print(f"✅ Région déjà existante: {region_name}")
                    region = existing_region
                    regions_existing += 1
                else:
                    # Créer la nouvelle région
                    region = await Region.create(name=region_name)
                    print(f"✨ Région créée: {region_name}")
                    regions_created += 1

                # Traiter les villes de cette région
                for ville_name in region_data["villes"]:
                    # Vérifier si la ville existe déjà
                    existing_city = await City.filter(name=ville_name).first()

                    if existing_city:
                        print(f"    ✅ Ville déjà existante: {ville_name}")
                        cities_existing += 1
                    else:
                        # Créer la nouvelle ville
                        await City.create(name=ville_name, region=region)
                        print(f"    ✨ Ville créée: {ville_name}")
                        cities_created += 1

        # Statistiques finales
        print("\n🎉 Seeding terminé!")
        print(f"   - Régions créées: {regions_created}")
        print(f"   - Régions déjà existantes: {regions_existing}")
        print(f"   - Villes créées: {cities_created}")
        print(f"   - Villes déjà existantes: {cities_existing}")
        print(f"   - Total des régions: {await Region.all().count()}")
        print(f"   - Total des villes: {await City.all().count()}")

    except Exception as e:
        print(f"❌ Erreur lors du seeding: {e}")
        raise
    finally:
        # Fermer les connexions
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(seed_regions_and_cities())
