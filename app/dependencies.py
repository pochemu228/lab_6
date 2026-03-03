from fastapi import HTTPException, status, Request
from typing import Set, Optional

from core.config import VALID_TOKENS

UNSAFE_METHODS: Set[str] = {"POST", "PUT", "PATCH", "DELETE"}

# ПРАВИЛЬНЫЙ ВАРИАНТ ДЛЯ ЧАСТИ 1: Токен из строки запроса
async def verify_token_query(
    request: Request,
    api_token: Optional[str] = None  # Токен из query параметра
) -> None:
    """
    Проверяет наличие и валидность токена для небезопасных методов.
    Токен ожидается в query параметре api_token.
    """
    # Проверяем только для небезопасных методов
    if request.method in UNSAFE_METHODS:
        # Если токен отсутствует или невалидный
        if not api_token or api_token not in VALID_TOKENS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing API token",
                headers={"WWW-Authenticate": "Bearer"}
            )
    # Для безопасных методов (GET, HEAD, OPTIONS) пропускаем без проверки
    return None
