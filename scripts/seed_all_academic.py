#!/usr/bin/env python3
"""
Script principal pour exécuter tous les seeds des domaines, niveaux et mentions
"""
import asyncio
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tortoise import Tortoise

from apps.tortoise.domain.models import Domain
from apps.tortoise.level.models import Level
from apps.tortoise.mention.models import Mention
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

# Données des niveaux d'étude basées sur les habilitations réelles
LEVELS_DATA = [
    {"name": "Licence", "acronym": "L"},
    {"name": "Master", "acronym": "M"},
    {"name": "Diplôme de Technicien Supérieur", "acronym": "DTS"},
    {"name": "Diplôme de Technicien Supérieur Spécialisé", "acronym": "DTSS"},
    {"name": "Doctorat", "acronym": "PhD"},
    {"name": "Diplôme d'Ingénieur", "acronym": "DI"},
]

# Données des mentions organisées par domaine basées sur les habilitations réelles
MENTIONS_DATA = {
    "Sciences de la Société": [
        "Droit",
        "Gestion",
        "Économie",
        "Sciences Politiques",
        "Communication",
        "Tourisme",
        "Management",
        "Administration",
        "Sociologie",
        "Anthropologie",
        "Philosophie",
        "Psychologie",
        "Langues",
        "Sciences Sociales",
        "Sciences de Gestion",
        "Sciences Juridiques",
        "Sciences Économiques",
        "Marketing",
        "Entrepreneuriat",
        "Commerce",
        "Finance",
        "Comptabilité",
    ],
    "Sciences et Technologies": [
        "Informatique",
        "Mathématiques",
        "Physique",
        "Chimie",
        "Biologie",
        "Géologie",
        "Sciences de la Terre",
        "Sciences Agronomiques",
        "Génie Civil",
        "Génie Industriel",
        "Électronique",
        "Télécommunication",
        "Électrotechnique",
        "Environnement",
        "Énergie Renouvelable",
        "BTP",
        "Technologie de l'Information",
        "Sciences de l'Ingénieur",
    ],
    "Sciences de la Santé": [
        "Médecine",
        "Pharmacie",
        "Vétérinaire",
        "Sage-femme",
        "Infirmier Généraliste",
        "Infirmier Anesthésiste",
        "Infirmier de Bloc Opératoire",
        "Technicien de Laboratoire",
        "Sciences Infirmières",
        "Maïeutique",
        "Kinésithérapeute",
        "Imagerie Médicale",
        "Administration Sanitaire",
    ],
    "Sciences de l'Ingénieur": [
        "Génie Civil",
        "Génie Industriel",
        "Génie Mécanique",
        "Génie Électrique",
        "Génie Informatique",
        "Génie Biomédical",
        "BTP",
        "Électronique",
        "Télécommunication",
        "Automatisme Industriel",
    ],
    "Sciences de l'Education": [
        "Pédagogie",
        "Technologie de l'Education",
        "Enseignements Littéraires",
        "Enseignements Scientifiques",
        "Formation des Formateurs",
    ],
    "Arts, Lettres et Sciences Humaines": [
        "Lettres",
        "Langues",
        "Histoire",
        "Géographie",
        "Philosophie",
        "Théologie",
        "Psychologie",
        "Anthropologie",
        "Communication",
        "Tourisme",
        "Création Artistique",
    ],
}


async def run_all_seeds():
    """Exécute tous les scripts de seed dans le bon ordre"""
    print("🚀 Démarrage du seeding complet...")
    print("=" * 50)

    # Initialiser Tortoise ORM
    await Tortoise.init(config=TORTOISE_ORM)

    try:
        # Étape 1: Seed des domaines
        print("\n📚 ÉTAPE 1: Seeding des domaines")
        print("-" * 30)
        await seed_domains_data()

        # Étape 2: Seed des niveaux
        print("\n🎓 ÉTAPE 2: Seeding des niveaux")
        print("-" * 30)
        await seed_levels_data()

        # Étape 3: Seed des mentions
        print("\n🎯 ÉTAPE 3: Seeding des mentions")
        print("-" * 30)
        await seed_mentions_data()

        # Statistiques finales
        print("\n" + "=" * 50)
        print("📊 STATISTIQUES FINALES")
        print("=" * 50)
        print(f"🏷️  Total des domaines: {await Domain.all().count()}")
        print(f"📈 Total des niveaux: {await Level.all().count()}")
        print(f"🎯 Total des mentions: {await Mention.all().count()}")
        print("\n✅ Seeding complet terminé avec succès!")

    except Exception as e:
        print(f"❌ Erreur lors du seeding complet: {e}")
        raise
    finally:
        await Tortoise.close_connections()


async def show_stats():
    """Affiche les statistiques actuelles de la base de données"""
    print("📊 STATISTIQUES ACTUELLES")
    print("=" * 30)

    await Tortoise.init(config=TORTOISE_ORM)

    try:
        domains_count = await Domain.all().count()
        levels_count = await Level.all().count()
        mentions_count = await Mention.all().count()

        print(f"🏷️  Domaines: {domains_count}")
        print(f"📈 Niveaux: {levels_count}")
        print(f"🎯 Mentions: {mentions_count}")

        if domains_count > 0:
            print("\n📚 Domaines existants:")
            domains = await Domain.all()
            for domain in domains:
                mentions_in_domain = await Mention.filter(domain=domain).count()
                print(f"   - {domain.name} ({mentions_in_domain} mentions)")

    except Exception as e:
        print(f"❌ Erreur lors de la récupération des statistiques: {e}")
    finally:
        await Tortoise.close_connections()


async def seed_domains_data():
    """Seed les domaines dans la base de données"""
    print("🌱 Seeding des domaines...")

    created_count = 0
    updated_count = 0

    for domain_data in DOMAINS_DATA:
        existing_domain = await Domain.filter(name=domain_data["name"]).first()

        if existing_domain:
            print(f"✅ Domaine '{domain_data['name']}' existe déjà")
            updated_count += 1
        else:
            domain = await Domain.create(name=domain_data["name"])
            print(f"✨ Domaine créé: {domain.name}")
            created_count += 1

    print(f"   - Domaines créés: {created_count}")
    print(f"   - Domaines déjà existants: {updated_count}")


async def seed_levels_data():
    """Seed les niveaux dans la base de données"""
    print("🌱 Seeding des niveaux...")

    created_count = 0
    updated_count = 0

    for level_data in LEVELS_DATA:
        existing_level = await Level.filter(acronym=level_data["acronym"]).first()

        if not existing_level:
            existing_level = await Level.filter(name=level_data["name"]).first()

        if existing_level:
            print(
                f"✅ Niveau '{level_data['name']}' ({level_data['acronym']}) existe déjà"
            )
            updated_count += 1
        else:
            level = await Level.create(
                name=level_data["name"], acronym=level_data["acronym"]
            )
            print(f"✨ Niveau créé: {level.name} ({level.acronym})")
            created_count += 1

    print(f"   - Niveaux créés: {created_count}")
    print(f"   - Niveaux déjà existants: {updated_count}")


async def seed_mentions_data():
    """Seed les mentions dans la base de données"""
    print("🌱 Seeding des mentions...")

    created_count = 0
    updated_count = 0
    domain_not_found_count = 0

    for domain_name, mentions in MENTIONS_DATA.items():
        domain = await Domain.filter(name=domain_name).first()
        if not domain:
            print(f"⚠️  Domaine '{domain_name}' non trouvé")
            domain_not_found_count += 1
            continue

        for mention_name in mentions:
            existing_mention = await Mention.filter(
                name=mention_name, domain=domain
            ).first()

            if existing_mention:
                print(f"✅ Mention '{mention_name}' existe déjà dans {domain_name}")
                updated_count += 1
            else:
                mention = await Mention.create(name=mention_name, domain=domain)
                print(f"✨ Mention créée: {mention.name} ({domain_name})")
                created_count += 1

    print(f"   - Mentions créées: {created_count}")
    print(f"   - Mentions déjà existantes: {updated_count}")
    print(f"   - Domaines non trouvés: {domain_not_found_count}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Script de seeding pour domaines, niveaux et mentions"
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Afficher seulement les statistiques sans faire de seeding",
    )

    args = parser.parse_args()

    if args.stats_only:
        asyncio.run(show_stats())
    else:
        asyncio.run(run_all_seeds())
