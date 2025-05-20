import os
import traceback

from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

print("--- DÉBUT DU SCRIPT DE TEST ---")

# Récupération de la configuration de la base de données depuis les variables d'environnement
db_user = os.getenv("DB_USERNAME", "votre_user_pg")
db_pass = os.getenv("DB_PASSWORD", "votre_pass_pg")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "votre_db_pg")

print(
    f"Variables d'environnement lues (DB_USER): {db_user}, (DB_HOST): {db_host}, (DB_PORT): {db_port}, (DB_NAME): {db_name}"
)

# Vérification si les variables essentielles sont définies
if not all(
    [db_user != "votre_user_pg", db_pass != "votre_pass_pg", db_name != "votre_db_pg"]
):
    print(
        "ERREUR: Des variables d'environnement de base de données essentielles (DB_USERNAME, DB_PASSWORD, DB_NAME) ne sont pas définies ou utilisent les valeurs par défaut."
    )
    print("Veuillez les configurer correctement avant de lancer le script.")
    print("--- FIN DU SCRIPT DE TEST (ERREUR DE CONFIGURATION) ---")
    exit(1)


connection_string = (
    f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
)
collection_name = "test_validation_collection_script"
embeddings_model = OpenAIEmbeddings()

try:
    print(f"Tentative de connexion avec : {connection_string}")
    print(f"Utilisation de la collection : {collection_name}")

    vectorstore = PGVector.from_documents(
        documents=[
            Document(
                page_content="Ceci est un contenu de test pour la validation via script.",
                metadata={"source": "test_script_file"},
            )
        ],
        embedding=embeddings_model,
        connection_string=connection_string,
        collection_name=collection_name,
        pre_delete_collection=True,
    )
    print("PGVector.from_documents exécuté avec succès.")

    results = vectorstore.similarity_search("contenu de test via script")
    print(f"Résultats de la recherche de similarité : {results}")

    if results and results[0].metadata.get("source") == "test_script_file":
        print("TEST RÉUSSI : Document trouvé et les métadonnées correspondent.")
        print(f"Métadonnées trouvées : {results[0].metadata}")
    elif results:
        print(
            "TEST ÉCHOUÉ : Document trouvé mais les métadonnées ne correspondent pas."
        )
        print(f"Métadonnées trouvées : {results[0].metadata}")
    else:
        print("TEST ÉCHOUÉ : Aucun document trouvé après la recherche de similarité.")

except Exception as e:
    print(f"Une erreur est survenue durant le test : {e}")
    print("Traceback:")
    print(traceback.format_exc())
finally:
    print("--- FIN DU SCRIPT DE TEST ---")
