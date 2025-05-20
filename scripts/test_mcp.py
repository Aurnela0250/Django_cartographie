import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Assurez-vous que le nom du package importé est correct,
# il est souvent mcp_client ou un nom similaire si mcp_use est le nom du repo/projet général.
# D'après le README, ça semble être MCPClient et MCPAgent directement depuis mcp_use.
from mcp_use import MCPAgent, MCPClient

# Charger les variables d'environnement (ex: OPENAI_API_KEY)
load_dotenv()

# Récupérer la clé API OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError(
        "La variable d'environnement OPENAI_API_KEY n'est pas définie. Veuillez la créer dans un fichier .env."
    )


def main():
    # Configuration du service MCP pour PostgreSQL
    db_url = "postgresql://cartographie:123456@localhost:5432/cartographie_db"
    mcp_postgres_port = "7000"  # Port sur lequel le serveur MCP écoutera

    # Structure de configuration conforme à la documentation officielle mcp_use
    config = {
        "mcpServers": {
            "postgres_service": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-postgres",
                    db_url,
                ],
                "env": {
                    # Ajoutez ici des variables d'environnement spécifiques si besoin
                    # Exemple : "PGSSLMODE": "prefer"
                },
            }
            # Vous pouvez ajouter d'autres serveurs ici
        }
    }

    print("Configuration MCP utilisée :")
    print(config)
    print("-" * 30)

    # Initialiser le client MCP à partir du dictionnaire de configuration
    client = MCPClient.from_dict(config)

    # Créer le modèle de langage Anthropic Claude 3 Haiku
    llm = ChatAnthropic(model="claude-3-haiku-20240307")

    # Création de l'agent MCP, restriction des outils dangereux
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        disallowed_tools=["file_system", "network", "shell"],
    )

    # Exemple de requête pour interagir avec le MCP Postgres
    query_postgres = (
        "Vérifie la structure ou le schéma de la base avant d'effectuer une requête. "
        "Quels sont les établissements qui offrent des formations en informatique ?"
    )
    # Autres exemples :
    # query_postgres = "Peux-tu lister les tables de la base de données en utilisant l'outil 'postgres_service' ?"
    # query_postgres = "En utilisant postgres_service, exécute la requête SQL 'SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';'"

    print(f"\nLancement de l'agent avec la requête :\n{query_postgres}")
    print("-" * 30)

    import asyncio

    try:
        # Gestion robuste de l'event loop pour compatibilité notebook/console
        async def run_agent():
            return await agent.run(query_postgres)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Si déjà dans un event loop (ex: notebook), utiliser create_task et attendre le résultat
            import nest_asyncio

            nest_asyncio.apply()
            task = loop.create_task(run_agent())
            result = loop.run_until_complete(task)
        else:
            result = asyncio.run(run_agent())

        print("\nRésultat de l'agent :")
        print(result)
    except Exception as e:
        print(f"\nUne erreur s'est produite lors de l'exécution de l'agent : {e}")
        print("Conseils de dépannage :")
        print(
            f"1. Vérifiez que votre base de données PostgreSQL est accessible à l'adresse : {db_url}"
        )
        print(
            f"2. Vérifiez qu'aucun autre service n'utilise le port {mcp_postgres_port} sur votre machine."
        )
        print(
            "3. Essayez de lancer manuellement la commande du serveur MCP dans un terminal pour voir les erreurs détaillées :"
        )
        cmd_str = f"npx -y @modelcontextprotocol/server-postgres --port {mcp_postgres_port} {db_url}"
        print(f"   Commande à tester : {cmd_str}")
        print(
            "4. Assurez-vous que '@modelcontextprotocol/server-postgres' est installable par npx."
        )


if __name__ == "__main__":
    main()
