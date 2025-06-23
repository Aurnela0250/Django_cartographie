#!/usr/bin/env python3
"""
Script de seed pour les mentions d'étude
Ce script nécessite que les domaines soient déjà créés
"""
import asyncio
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tortoise import Tortoise

from apps.tortoise.domain.models import Domain
from apps.tortoise.mention.models import Mention
from config.settings import TORTOISE_ORM

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


async def seed_mentions():
    """Seed les mentions dans la base de données"""
    print("🌱 Démarrage du seeding des mentions...")

    # Initialiser Tortoise ORM
    await Tortoise.init(config=TORTOISE_ORM)

    try:
        # Compter les mentions existantes
        existing_count = await Mention.all().count()
        print(f"📊 Nombre de mentions existantes: {existing_count}")

        created_count = 0
        updated_count = 0
        domain_not_found_count = 0

        for domain_name, mentions in MENTIONS_DATA.items():
            print(f"\n🔍 Traitement du domaine: {domain_name}")

            # Trouver le domaine
            domain = await Domain.filter(name=domain_name).first()
            if not domain:
                print(f"⚠️  Domaine '{domain_name}' non trouvé, passage au suivant")
                domain_not_found_count += 1
                continue

            for mention_name in mentions:
                # Vérifier si la mention existe déjà
                existing_mention = await Mention.filter(
                    name=mention_name, domain=domain
                ).first()

                if existing_mention:
                    print(f"✅ Mention '{mention_name}' existe déjà dans {domain_name}")
                    updated_count += 1
                else:
                    # Créer la nouvelle mention
                    mention = await Mention.create(name=mention_name, domain=domain)
                    print(f"✨ Mention créée: {mention.name} ({domain_name})")
                    created_count += 1

        print("\n🎉 Seeding terminé!")
        print(f"   - Mentions créées: {created_count}")
        print(f"   - Mentions déjà existantes: {updated_count}")
        print(f"   - Domaines non trouvés: {domain_not_found_count}")
        print(f"   - Total des mentions: {await Mention.all().count()}")

        if domain_not_found_count > 0:
            print(
                "\n💡 Conseil: Exécutez d'abord le script seed_domains.py pour créer les domaines manquants"
            )

    except Exception as e:
        print(f"❌ Erreur lors du seeding: {e}")
        raise
    finally:
        # Fermer les connexions
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(seed_mentions())
