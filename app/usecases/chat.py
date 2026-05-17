from app.db.models import ChatMessage
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(self, messages: ChatMessageRepository, llm_client: OpenRouterClient) -> None:
        self._messages = messages
        self._llm_client = llm_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None,
        max_history: int,
        temperature: float,
    ) -> str:
        llm_messages: list[dict[str, str]] = []
        if system:
            llm_messages.append({"role": "system", "content": system})

        history = await self._messages.get_latest(user_id=user_id, limit=max_history)
        llm_messages.extend({"role": item.role, "content": item.content} for item in history)
        llm_messages.append({"role": "user", "content": prompt})

        await self._messages.add(user_id=user_id, role="user", content=prompt)
        answer = await self._llm_client.chat_completion(
            messages=llm_messages,
            temperature=temperature,
        )
        await self._messages.add(user_id=user_id, role="assistant", content=answer)
        return answer

    async def get_history(self, user_id: int, limit: int = 50) -> list[ChatMessage]:
        return await self._messages.get_latest(user_id=user_id, limit=limit)

    async def clear_history(self, user_id: int) -> None:
        await self._messages.clear_for_user(user_id)
