from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user_id: int, role: str, content: str) -> ChatMessage:
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_latest(self, user_id: int, limit: int) -> list[ChatMessage]:
        if limit <= 0:
            return []

        statement = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc(), ChatMessage.id.desc())
            .limit(limit)
        )
        result = await self._session.execute(statement)
        return list(reversed(result.scalars().all()))

    async def clear_for_user(self, user_id: int) -> None:
        await self._session.execute(delete(ChatMessage).where(ChatMessage.user_id == user_id))
        await self._session.commit()
