from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

from core.services.jwt_service import JWTService, SoketToken

@database_sync_to_async
def get_user(token):
    try:
        user = JWTService.validate_token(token, SoketToken)
        print(f"User validated: {user}")  # Добавлено логирование
        return user
    except Exception as e:
        print(f"Error validating token: {e}")  # Добавлено логирование
        return None



class AuthSocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = (
            dict(
                [item.split('=') for item in scope['query_string'].decode('utf-8').split('&') if item]
            ).get('token', None)
        )
        scope['user'] = await get_user(token) if token else None
        return await super().__call__(scope, receive, send)



