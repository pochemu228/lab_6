import secrets
from typing import FrozenSet


VALID_TOKENS: FrozenSet[str] = frozenset([
    secrets.token_hex(16),  # 32 символа
    secrets.token_hex(16),
    secrets.token_hex(16),
    secrets.token_hex(16),
    secrets.token_hex(16)
])

print(f"Сгенерированные токены: {VALID_TOKENS}")