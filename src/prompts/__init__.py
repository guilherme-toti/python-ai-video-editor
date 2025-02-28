from dataclasses import dataclass


@dataclass
class Prompt:
    user_prompt: str
    system_prompt: str
