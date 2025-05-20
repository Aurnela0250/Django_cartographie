import logging

from ninja_extra import api_controller, http_get, http_post

from core.use_cases.chatbot_usecase import ChatbotUseCase
from core.use_cases.index_data_usecase import IndexDataUseCase
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.schemas.chat_schema import (
    ChatHistoryResponseSchema,
    ChatInputSchema,
    ChatResponseSchema,
)


@api_controller("/chat", tags=["Chatbot"])
class ChatController:
    """Contrôleur pour le chatbot et l'indexation RAG"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.index_usecase = IndexDataUseCase()
        self.chatbot_usecase = ChatbotUseCase()

    @http_post("/index-data", response={200: dict, 500: dict})
    def index_data(self, request):
        try:
            success, message = self.index_usecase.index_documents()
            if success:
                return 200, {"success": True, "message": message}
            else:
                return 500, {"success": False, "message": message}
        except Exception as e:
            self.logger.error(f"Erreur indexation: {e}", exc_info=True)
            return 500, {"success": False, "message": str(e)}

    @http_post(
        "",
        auth=jwt_auth,
        response={200: ChatResponseSchema, 401: dict, 500: dict},
    )
    def chat(self, request, payload: ChatInputSchema):
        user_id = request.auth.get("user_id")
        if not user_id:
            return 401, {"detail": "Utilisateur non authentifié."}
        try:
            response, history = self.chatbot_usecase.chat(user_id, payload.message)
            return 200, {
                "user_id": user_id,
                "response": response,
                "history": history,
            }
        except Exception as e:
            self.logger.error(f"Erreur lors du chat: {e}")
            return 500, {"detail": f"Erreur lors du chat : {e}"}

    @http_get(
        "/history",
        auth=jwt_auth,
        response={200: ChatHistoryResponseSchema, 401: dict},
    )
    def chat_history(self, request):
        user_id = request.auth.get("user_id")
        if not user_id:
            return 401, {"detail": "Utilisateur non authentifié."}
        history = self.chatbot_usecase.get_history(user_id)
        return 200, {"user_id": user_id, "history": history}
