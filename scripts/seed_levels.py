#!/usr/bin/env python3
"""
Script de seed pour les niveaux d'étude
"""
import asyncio
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tortoise import Tortoise

from apps.tortoise.level.models import Level
from config.settings import TORTOISE_ORM

# Données des niveaux d'étude basées sur les habilitations réelles
LEVELS_DATA = [
    {"name": "Licence", "acronym": "L"},
    {"name": "Master", "acronym": "M"},
    {"name": "Diplôme de Technicien Supérieur", "acronym": "DTS"},
    {"name": "Diplôme de Technicien Supérieur Spécialisé", "acronym": "DTSS"},
    {"name": "Doctorat", "acronym": "PhD"},
    {"name": "Diplôme d'Ingénieur", "acronym": "DI"},
]


async def seed_levels():
    """Seed les niveaux dans la base de données"""
    print("🌱 Démarrage du seeding des niveaux d'étude...")

    # Initialiser Tortoise ORM
    await Tortoise.init(config=TORTOISE_ORM)

    try:
        # Compter les niveaux existants
        existing_count = await Level.all().count()
        print(f"📊 Nombre de niveaux existants: {existing_count}")

        created_count = 0
        updated_count = 0

        for level_data in LEVELS_DATA:
            # Vérifier si le niveau existe déjà (par acronyme ou nom)
            existing_level = await Level.filter(acronym=level_data["acronym"]).first()

            if not existing_level:
                existing_level = await Level.filter(name=level_data["name"]).first()

            if existing_level:
                print(
                    f"✅ Niveau '{level_data['name']}' ({level_data['acronym']}) existe déjà"
                )
                updated_count += 1
            else:
                # Créer le nouveau niveau
                level = await Level.create(
                    name=level_data["name"], acronym=level_data["acronym"]
                )
                print(f"✨ Niveau créé: {level.name} ({level.acronym})")
                created_count += 1

        print("\n🎉 Seeding terminé!")
        print(f"   - Niveaux créés: {created_count}")
        print(f"   - Niveaux déjà existants: {updated_count}")
        print(f"   - Total des niveaux: {await Level.all().count()}")

    except Exception as e:
        print(f"❌ Erreur lors du seeding: {e}")
        raise
    finally:
        # Fermer les connexions
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(seed_levels())
