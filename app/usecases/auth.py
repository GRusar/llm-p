from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UserRepository


class AuthUseCase:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def register(self, email: str, password: str) -> User:
        existing_user = await self._users.get_by_email(email)
        if existing_user is not None:
            raise ConflictError("Email already exists")

        return await self._users.create(email=email, password_hash=hash_password(password))

    async def login(self, email: str, password: str) -> str:
        user = await self._users.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        return create_access_token(user_id=user.id, role=user.role)

    async def get_profile(self, user_id: int) -> User:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")

        return user
