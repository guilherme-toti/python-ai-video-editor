import os
from typing import Optional

import openai
from dotenv import load_dotenv


class OpenAI:
    def __init__(self):
        load_dotenv()

        self.client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def request(
        self,
        system_prompt: str,
        user_prompt: str,
        options: Optional[dict] = None,
    ) -> str:
        if options is None:
            options = dict()

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
            max_completion_tokens=16000,
            **options,
        )

        result = []
        for chunk in response:
            result.append(chunk.choices[0].delta.content)

        result = [m for m in result if m is not None]
        full_result = ''.join(result)

        return full_result
