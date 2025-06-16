import os


def create_tortoise_structure():
    django_apps_base_dir = (
        "/Users/ninotwilrich/Documents/au_projet/Django_cartographie/apps/django"
    )
    tortoise_apps_base_dir = (
        "/Users/ninotwilrich/Documents/au_projet/Django_cartographie/apps/tortoise"
    )

    # Assurez-vous que le répertoire de base des applications Tortoise existe
    os.makedirs(tortoise_apps_base_dir, exist_ok=True)
    print(f"Base Tortoise directory ensured: {tortoise_apps_base_dir}")

    if not os.path.exists(django_apps_base_dir):
        print(f"Error: Django apps directory not found at {django_apps_base_dir}")
        return

    for item_name in os.listdir(django_apps_base_dir):
        django_item_path = os.path.join(django_apps_base_dir, item_name)

        if os.path.isdir(django_item_path):
            app_name = item_name
            print(f"Processing Django app: {app_name}")

            # Créer le dossier correspondant dans Tortoise
            tortoise_app_dir = os.path.join(tortoise_apps_base_dir, app_name)
            os.makedirs(tortoise_app_dir, exist_ok=True)
            print(f"  Created Tortoise app directory: {tortoise_app_dir}")

            # Créer models.py
            models_file_path = os.path.join(tortoise_app_dir, "models.py")
            if not os.path.exists(models_file_path):
                with open(models_file_path, "w") as f:
                    f.write("# Tortoise ORM models for app: " + app_name + "\n")
                    f.write("from tortoise.models import Model\n")
                    f.write("from tortoise import fields\n")
                print(f"    Created models.py: {models_file_path}")
            else:
                print(f"    models.py already exists: {models_file_path}")

            # Créer __init__.py
            init_file_path = os.path.join(tortoise_app_dir, "__init__.py")
            if not os.path.exists(init_file_path):
                with open(init_file_path, "w") as f:
                    pass  # Créer un fichier vide
                print(f"    Created __init__.py: {init_file_path}")
            else:
                print(f"    __init__.py already exists: {init_file_path}")
        else:
            print(f"Skipping non-directory item: {item_name}")

    print("\nScript finished.")


if __name__ == "__main__":
    create_tortoise_structure()
