import json
import logging
import os

from langchain_community.vectorstores.pgvector import PGVector  # MODIFIÉ

# UPDATED Import
from langchain_core.documents import (
    Document,  # Changed from langchain.docstore.document
)
from langchain_openai import OpenAIEmbeddings

# Optional: Define constants at the module level if they are truly fixed
# Or keep them as instance attributes if they might vary per instance/config
DEFAULT_JSON_DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "../../presentation/jsons/etablissements_data.json",
)
DEFAULT_COLLECTION_NAME = "etablissements_formations_rag"


class IndexDataUseCase:
    def __init__(self, json_data_file: str | None = None):  # Changed type hint
        self.logger = logging.getLogger(__name__)
        self.embeddings_model = OpenAIEmbeddings()
        self.collection_name = DEFAULT_COLLECTION_NAME  # Using constant
        self.json_data_file = json_data_file or DEFAULT_JSON_DATA_FILE
        self.connection_string = self._get_connection_string()

    def _get_connection_string(self) -> str:  # Added return type hint
        DB_USER = os.getenv("DB_USERNAME", "votre_user_pg")
        DB_PASS = os.getenv("DB_PASSWORD", "votre_pass_pg")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME", "votre_db_pg")
        return (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    def load_and_prepare_documents(self) -> list[Document]:  # Added return type hint
        langchain_documents = []
        try:
            with open(self.json_data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_establishments_data = data.get("items", [])
                if not all_establishments_data:
                    self.logger.warning("No items found in the JSON data file.")
                    return []
        except FileNotFoundError:
            self.logger.error(f"JSON data file not found: {self.json_data_file}")
            return []
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Error decoding JSON from file {self.json_data_file}: {e}",
                exc_info=True,
            )
            return []
        except Exception as e:
            # Keep the print for immediate feedback if running from CLI, logger for persistent logs
            print(f"Erreur inattendue lors de la lecture du fichier JSON : {e}")
            self.logger.error(
                f"Erreur inattendue lors de la lecture du fichier JSON : {e}",
                exc_info=True,
            )
            return []

        for etab_data in all_establishments_data:
            etab_name = etab_data.get("name", "N/A")
            # Simplified `get` with default for nested dictionaries
            etab_acronyme = etab_data.get(
                "acronyme", ""
            )  # Default empty string is fine if that's intended
            etab_address = etab_data.get("address", "Adresse non spécifiée")
            etab_type = etab_data.get("establishment_type", {}).get(
                "name", "Type non spécifié"
            )
            etab_sector = etab_data.get("sector", {}).get(
                "name", "Secteur non spécifié"
            )

            # etab_city_name seems to be a duplicate of etab_address in your original code.
            # If it's intended to be just the city, you'd need logic to extract it.
            # Assuming it's the full address for now based on original usage.
            etab_city_name = etab_address

            etab_description = (
                etab_data.get("description")
                or "Aucune description générale de l'établissement."
            )

            for form_data in etab_data.get("formations", []):
                formation_intitule = form_data.get("intitule", "Intitulé non spécifié")
                formation_level = form_data.get("level", {}).get(
                    "name", "Niveau non spécifié"
                )
                formation_mention = form_data.get("mention", {}).get(
                    "name", "Mention non spécifiée"
                )
                formation_duration = form_data.get(
                    "duration"
                )  # Remains None if not present
                # Corrected handling for authorization status
                auth_data = form_data.get("authorization")
                if isinstance(auth_data, dict):
                    formation_auth_status = auth_data.get(
                        "status", "Statut d'autorisation inconnu"
                    )
                else:
                    formation_auth_status = "Statut d'autorisation inconnu"

                formation_description = (
                    form_data.get("description")
                    or "Aucune description spécifique pour cette formation."
                )

                content_parts = [
                    f"Établissement : {etab_name} ({etab_acronyme if etab_acronyme else 'N/A'}). Type : {etab_type}. Secteur : {etab_sector}. Adresse : {etab_address}.",
                    f"Description de l'établissement : {etab_description}",
                    "Formation proposée :",
                    f"- Intitulé : {formation_intitule}",
                    f"- Niveau : {formation_level}",
                    f"- Mention/Domaine : {formation_mention}",
                ]
                if formation_duration is not None:  # Check for None explicitly
                    content_parts.append(f"- Durée : {formation_duration} mois.")
                content_parts.append(
                    f"- Statut de l'autorisation : {formation_auth_status}."
                )
                # Only add formation description if it's not the default placeholder
                if (
                    formation_description
                    != "Aucune description spécifique pour cette formation."
                ):
                    content_parts.append(
                        f"- Description de la formation : {formation_description}."
                    )

                page_content = "\n".join(content_parts)

                metadata = {
                    "establishment_id": str(etab_data.get("id", "N/A")),
                    "establishment_name": etab_name,
                    "establishment_acronyme": etab_acronyme,
                    "address": etab_address,
                    "city": etab_city_name,  # As discussed, this is full address currently
                    "establishment_type": etab_type,
                    "sector": etab_sector,
                    "formation_id": str(form_data.get("id", "N/A")),
                    "formation_intitule": formation_intitule,
                    "formation_level": formation_level,
                    "formation_mention": formation_mention,
                    "formation_duration_months": formation_duration,  # Can be None
                    "authorization_status": formation_auth_status,
                    "site_url": etab_data.get("site_url"),  # Can be None
                    "contacts": etab_data.get("contacts"),  # Can be None
                }
                # Cleaning None values is good, especially for vector store metadata
                metadata_cleaned = {k: v for k, v in metadata.items() if v is not None}
                langchain_documents.append(
                    Document(page_content=page_content, metadata=metadata_cleaned)
                )

        if not langchain_documents:
            self.logger.warning("No documents were prepared from the JSON data.")
        return langchain_documents

    def index_documents(
        self, batch_size: int = 32
    ) -> tuple[bool, str]:  # Added type hints
        documents_to_index = self.load_and_prepare_documents()
        if not documents_to_index:
            self.logger.warning("No documents to index.")
            return False, "Aucun document à indexer."

        try:
            total = len(documents_to_index)
            self.logger.info(
                f"Indexation par batch de {batch_size} documents (total: {total})"
            )

            # PGVector.from_documents now handles pre_delete_collection internally for the first call
            # if the collection exists and you want to replace it.
            # The `pre_delete_collection=True` on the first call is a good pattern.

            # Delete the collection once before starting batching
            # This requires creating a PGVector instance first to call delete_collection
            # Or, rely on pre_delete_collection in the first from_documents call.
            # Let's stick to your original logic as it's clear.

            first_batch = True
            for i in range(0, total, batch_size):
                batch_docs = documents_to_index[i : i + batch_size]
                PGVector.from_documents(
                    documents=batch_docs,
                    embedding=self.embeddings_model,
                    collection_name=self.collection_name,
                    connection_string=self.connection_string,
                    pre_delete_collection=first_batch,  # This will delete if it's the first batch
                )
                first_batch = False  # Ensure it's only deleted once
                self.logger.info(
                    f"Batch {i//batch_size+1}/{total//batch_size+1 if total % batch_size == 0 else total//batch_size+2}: {len(batch_docs)} documents indexés."
                )
            return (
                True,
                f"Indexation terminée. {total} documents indexés en batchs de {batch_size}.",
            )
        except Exception as e:
            # Keep the print for immediate feedback if running from CLI, logger for persistent logs
            print(f"Erreur lors de l'indexation : {e}")
            self.logger.error(f"Erreur lors de l'indexation : {e}", exc_info=True)
            return (
                False,
                f"Erreur lors de l'indexation : {str(e)}",
            )  # Pass string representation of e
