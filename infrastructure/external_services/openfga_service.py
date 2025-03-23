from django.conf import settings
from openfga_sdk import OpenFgaClient, ClientConfiguration
from openfga_sdk.client.models import WriteRequest, TupleKey

from presentation.exceptions import InternalServerError


class OpenFGAService:
    def __init__(self):
        self.client = OpenFgaClient(
            ClientConfiguration(
                api_url=settings.FGA_API_URL,
                store_id=settings.FGA_STORE_ID,
                authorization_model_id=settings.FGA_MODEL_ID,
            )
        )

    async def check_permission(self, user_id: str, relation: str, resource: str):
        try:
            response = await self.client.check(
                user=f"user:{user_id}",
                relation=relation,
                object=resource,
            )
            return response.allowed
        except Exception as e:
            raise InternalServerError(detail=str(e))

    async def create_relationship(self, user: str, relation: str, object: str):
        try:
            tuple_key = TupleKey(user=user, relation=relation, object=object)
            write_request = WriteRequest(writes=[tuple_key])
            await self.client.write(body=write_request)
            return True
        except Exception as e:
            raise InternalServerError(detail=str(e))

    # Add other methods as needed
