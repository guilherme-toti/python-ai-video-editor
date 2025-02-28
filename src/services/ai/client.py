from typing import Protocol, Optional


class AIClient(Protocol):
    def request(self, system_prompt: str, user_prompt: str, options: Optional[dict] = None) -> str: ...
