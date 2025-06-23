#!/usr/bin/env python3
"""
Script de seed pour les domaines d'étude
"""
import asyncio
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tortoise import Tortoise

from apps.tortoise.domain.models import Domain
from config.settings import TORTOISE_ORM

# Données des domaines d'étude basées sur les habilitations réelles
DOMAINS_DATA = [
    {"name": "Sciences de la Société"},
    {"name": "Sciences et Technologies"},
    {"name": "Sciences de la Santé"},
    {"name": "Sciences de l'Ingénieur"},
    {"name": "Sciences de l'Education"},
    {"name": "Arts, Lettres et Sciences Humaines"},
]


async def seed_domains():
    """Seed les domaines dans la base de données"""
    print("🌱 Démarrage du seeding des domaines...")

    # Initialiser Tortoise ORM
    await Tortoise.init(config=TORTOISE_ORM)

    try:
        # Compter les domaines existants
        existing_count = await Domain.all().count()
        print(f"📊 Nombre de domaines existants: {existing_count}")

        created_count = 0
        updated_count = 0

        for domain_data in DOMAINS_DATA:
            # Vérifier si le domaine existe déjà
            existing_domain = await Domain.filter(name=domain_data["name"]).first()

            if existing_domain:
                print(f"✅ Domaine '{domain_data['name']}' existe déjà")
                updated_count += 1
            else:
                # Créer le nouveau domaine
                domain = await Domain.create(name=domain_data["name"])
                print(f"✨ Domaine créé: {domain.name}")
                created_count += 1

        print("\n🎉 Seeding terminé!")
        print(f"   - Domaines créés: {created_count}")
        print(f"   - Domaines déjà existants: {updated_count}")
        print(f"   - Total des domaines: {await Domain.all().count()}")

    except Exception as e:
        print(f"❌ Erreur lors du seeding: {e}")
        raise
    finally:
        # Fermer les connexions
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(seed_domains())
