from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from config import SECRET_JWT_WORD

bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_JWT_WORD, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)   