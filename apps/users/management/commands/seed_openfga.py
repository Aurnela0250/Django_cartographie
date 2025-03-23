import asyncio

from django.core.management.base import BaseCommand

from infrastructure.external_services.openfga_service import OpenFGAService


async def seed_openfga_relations():
    openfga_service = OpenFGAService()

    # Créer une équipe par défaut
    default_team_id = "lemon"

    # Configurer les relations pour endpoint
    # //! Client to endpoint:school
    await openfga_service.create_relationship(
        f"team:{default_team_id}#client", "create_school", "endpoint:school"
    )
    await openfga_service.create_relationship(
        f"team:{default_team_id}#client", "update_school", "endpoint:school"
    )
    await openfga_service.create_relationship(
        f"team:{default_team_id}#client", "delete_school", "endpoint:school"
    )
    await openfga_service.create_relationship(
        f"team:{default_team_id}#client", "read_school", "endpoint:school"
    )
    # //! Admin to endpoint:school
    await openfga_service.create_relationship(
        f"team:{default_team_id}#admin", "create_school", "endpoint:school"
    )
    await openfga_service.create_relationship(
        f"team:{default_team_id}#admin", "update_school", "endpoint:school"
    )
    await openfga_service.create_relationship(
        f"team:{default_team_id}#admin", "delete_school", "endpoint:school"
    )
    await openfga_service.create_relationship(
        f"team:{default_team_id}#admin", "read_school", "endpoint:school"
    )

    # //! user to endpoint:school
    await openfga_service.create_relationship(
        f"team:{default_team_id}#user", "read_school", "endpoint:school"
    )
    await openfga_service.create_relationship(
        f"team:{default_team_id}#user", "update_school", "endpoint:school"
    )

    print("OpenFGA relations seeded successfully.")


class Command(BaseCommand):
    help = "Seeds the OpenFGA relations"

    def handle(self, *args, **options):
        asyncio.run(seed_openfga_relations())
        self.stdout.write(self.style.SUCCESS("Successfully seeded OpenFGA relations"))
