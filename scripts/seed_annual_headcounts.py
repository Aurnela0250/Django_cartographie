import os
import random

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.formation.models import AnnualHeadcount, Formation

formations = Formation.objects.all()
years = list(range(2014, 2024 + 1))
count = 0

for formation in formations:
    for year in years:
        students = random.randint(50, 250)
        success_rate = round(random.uniform(70, 100), 1)
        # Vérifier si déjà existant (éviter doublons)
        if not AnnualHeadcount.objects.filter(
            formation=formation, academic_year=year
        ).exists():
            AnnualHeadcount.objects.create(
                formation=formation,
                academic_year=year,
                students=students,
                success_rate=success_rate,
            )
            count += 1
print(f"Seed terminé : {count} AnnualHeadcount créés.")
