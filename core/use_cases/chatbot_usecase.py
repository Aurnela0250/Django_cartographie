import json  # AJOUTÉ
import os
from typing import Any, Dict, List  # For type hinting

from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores.pgvector import PGVector  # MODIFIÉ
from langchain_core.documents import Document  # For type hinting format_docs
from langchain_core.output_parsers import (
    JsonOutputParser,  # UPDATED: For structured JSON output
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_openai import OpenAIEmbeddings

# from langchain_core.pydantic_v1 import BaseModel, Field # If using PydanticOutputParser
from infrastructure.external_services.redis_service import (
    RedisService,  # Assuming this is correctly defined
)

# Define constants at the module level
DEFAULT_COLLECTION_NAME = "etablissements_formations_rag"
REDIS_EXPIRE_SECONDS = 3600  # 1h

# Optional: Define Pydantic models for structured output (recommended for complex JSON)
# This makes the JsonOutputParser (or PydanticOutputParser) more robust.
# Example (you'd need to fill this out completely based on your desired JSON structure):
# class FormationDetail(BaseModel):
#     title: str
#     level: str
#     domain_mention: str
#     description: Optional[str] = None
#     authorization_status: Optional[str] = None

# class FoundDataItem(BaseModel):
#     establishment_name: str
#     establishment_acronym: Optional[str] = None
#     type: Optional[str] = None
#     sector: Optional[str] = None
#     address: str
#     site_url: Optional[str] = None
#     description: Optional[str] = None
#     formations: List[FormationDetail]

# class ChatResponse(BaseModel):
#     assistant_message: str
#     found_data: List[FoundDataItem]
#     clarification_question: Optional[str] = None

RAG_PROMPT_TEMPLATE = """
Vous êtes un assistant IA amical et conversationnel, spécialisé dans l'orientation vers des établissements d'enseignement supérieur et leurs formations.
Votre objectif est d'aider l'utilisateur à trouver les informations les plus pertinentes en fonction de ses besoins.
Utilisez UNIQUEMENT le CONTEXTE fourni ci-dessous pour formuler vos réponses. Ne faites aucune supposition et n'inventez pas d'informations.

CONTEXTE:
{context}

QUESTION DE L'UTILISATEUR:
{question}

INSTRUCTIONS POUR LA RÉPONSE:
Votre réponse DOIT respecter le format JSON suivant. Assurez-vous que le JSON est valide.

{{
  "assistant_message": "string",
  "found_data": [
    {{
      "establishment_name": "Nom de l'établissement",
      "establishment_acronym": "Acronyme (si disponible)",
      "type": "Type d'établissement (si disponible)",
      "sector": "Secteur (si disponible)",
      "address": "Adresse de l'établissement",
      "site_url": "URL du site (si disponible dans le contexte)",
      "description": "Courte description de l'établissement (si disponible)",
      "formations": [
        {{
          "title": "Intitulé de la Formation",
          "level": "Niveau (Licence, Master, etc.)",
          "domain_mention": "Domaine ou mention principale",
          "description": "Description de la formation (si disponible)",
          "authorization_status": "Statut de l'autorisation (si disponible)"
        }}
      ]
    }}
  ],
  "clarification_question": "string ou null"
}}

RÈGLES SPÉCIFIQUES POUR LE CONTENU DU JSON:
1.  **Ton et Style Général** : Adoptez un ton chaleureux et engageant dans le message principal de l'assistant (`assistant_message`).
2.  **Analyse de la Question** : Identifiez les critères clés dans la demande de l'utilisateur (nom de formation, niveau, ville, type d'établissement, etc.) pour peupler la section `found_data`.
3.  **Peuplement de `found_data`** :
    Si le CONTEXTE contient des informations pertinentes, structurez chaque élément du tableau `found_data` comme décrit dans le format JSON ci-dessus.
    Regroupez les formations par établissement. Si aucune donnée pertinente n'est trouvée, `found_data` doit être une liste vide (`[]`).
4.  **Gestion des Questions Vagues** :
    Si la question de l'utilisateur est trop vague pour fournir une réponse précise (par exemple, "Je cherche une formation"), le JSON de réponse doit :
    *   Avoir un `assistant_message` approprié (par exemple, "Je peux vous aider à trouver une formation ! Pour mieux vous guider...").
    *   Inclure une `clarification_question` (par exemple, "Pourriez-vous me préciser le domaine d'études, le niveau (Licence, Master, etc.) ou peut-être une ville en particulier ?").
    *   Avoir `found_data` comme une liste vide (`[]`).
5.  **Gestion des Informations Non Trouvées** :
    Si le CONTEXTE ne contient aucune information pertinente pour la question (et que la question n'est pas vague), le JSON de réponse doit :
    *   Avoir un `assistant_message` qui l'indique poliment (par exemple, "Je n'ai pas trouvé d'informations correspondant exactement à votre recherche actuelle. Pourrions-nous essayer avec d'autres mots-clés ou critères ?").
    *   Avoir `found_data` comme une liste vide (`[]`).
    *   Mettre `clarification_question` à `null` ou l'omettre (si le parser JSON le gère) sauf si une clarification est réellement nécessaire pour une nouvelle tentative.
6.  **Pertinence et Concision** : Ne listez dans `found_data` que les informations directement en lien avec la question. Soyez factuel. Le message dans `assistant_message` doit être concis.

RÉPONSE ASSISTANT (doit être un objet JSON valide et unique respectant la structure et les règles décrites ci-dessus):
"""


class ChatbotUseCase:
    def __init__(self):
        self.llm = ChatAnthropic(model_name="claude-3-haiku-20240307")
        self.embeddings_model = OpenAIEmbeddings()
        self.collection_name = DEFAULT_COLLECTION_NAME
        self.connection_string = self._get_connection_string()
        self.redis_expire = REDIS_EXPIRE_SECONDS
        # Initialize the output parser. If you defined Pydantic models:
        # self.output_parser = PydanticOutputParser(pydantic_object=ChatResponse)
        # For now, using JsonOutputParser
        self.output_parser = JsonOutputParser()

    def _get_connection_string(self) -> str:
        DB_USER = os.getenv("DB_USERNAME", "votre_user_pg")
        DB_PASS = os.getenv("DB_PASSWORD", "votre_pass_pg")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME", "votre_db_pg")
        return (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    def _get_retriever(
        self,
    ):  # Consider adding return type hint: -> VectorStoreRetriever
        vectorstore = PGVector(
            connection_string=self.connection_string,  # MODIFIÉ: connection -> connection_string
            collection_name=self.collection_name,
            embedding_function=self.embeddings_model,  # MODIFIÉ: embeddings -> embedding_function
            use_jsonb=True,  # Good for metadata filtering if PGVector supports it well here
            # pre_delete_collection=False, # Correct for retriever, it should not delete
        )
        return vectorstore.as_retriever(
            search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10}
        )

    def _format_docs(self, docs: List[Document]) -> str:  # Added type hint for docs
        if not docs:
            return "Aucune information pertinente trouvée dans la base de données pour cette requête."
        return "\n\n---\n\n".join(
            [
                f"Source {i+1}:\n{doc.page_content}\nMétadonnées: {doc.metadata}"
                for i, doc in enumerate(docs)
            ]
        )

    def _get_rag_chain(
        self, retriever_instance
    ) -> RunnableSerializable[str, Dict[str, Any]]:
        # Updated prompt template to include format instructions from the parser if needed
        # For JsonOutputParser, it often suffices to tell the LLM to output JSON.
        # PydanticOutputParser can inject more detailed format instructions.
        prompt_with_format_instructions = RAG_PROMPT_TEMPLATE
        # If using PydanticOutputParser, you might append:
        # prompt_with_format_instructions += "\n\n{format_instructions}\n"

        rag_prompt = ChatPromptTemplate.from_template(prompt_with_format_instructions)

        # If using PydanticOutputParser, partial the prompt with format instructions
        # partial_prompt = rag_prompt.partial(format_instructions=self.output_parser.get_format_instructions())

        rag_chain = (
            {
                "context": retriever_instance | self._format_docs,
                "question": RunnablePassthrough(),
            }
            | rag_prompt  # Use partial_prompt here if using PydanticOutputParser
            | self.llm
            | self.output_parser  # Use the JSON output parser
        )
        return rag_chain

    def chat(
        self, user_id: str, user_message: str
    ) -> tuple[Dict[str, Any], list[bytes]]:
        redis_client = RedisService.get_client()
        retriever = self._get_retriever()
        rag_chain = self._get_rag_chain(retriever)
        redis_key = f"chat_history:{user_id}"

        # Récupère l'historique (sous forme de liste de bytes)
        history_bytes = redis_client.lrange(redis_key, 0, -1)
        # Decode history for potential use (though not used in this RAG chain directly)
        # history_decoded = [h.decode('utf-8') for h in history_bytes]

        # Ajoute la question courante
        redis_client.rpush(
            redis_key, f"Q: {user_message}"
        )  # rpush expects bytes or strings
        redis_client.expire(redis_key, self.redis_expire)

        # Génère la réponse (now a dictionary/parsed JSON)
        response_data: Dict[str, Any] = rag_chain.invoke(user_message)

        # Stocke la réponse (convert dict to string for Redis if necessary)
        # Best to store JSON as a string in Redis
        response_str = json.dumps(response_data, ensure_ascii=False)
        redis_client.rpush(redis_key, f"A: {response_str}")
        redis_client.expire(redis_key, self.redis_expire)

        return (
            response_data,
            history_bytes,
        )  # Return the parsed JSON and raw history bytes

    def get_history(self, user_id: str) -> list[bytes]:
        redis_client = RedisService.get_client()
        redis_key = f"chat_history:{user_id}"
        return redis_client.lrange(redis_key, 0, -1)  # Returns list of bytes
