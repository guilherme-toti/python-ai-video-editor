import os
from typing import Tuple, List

from rich.progress import Progress

from src.prompts.content import (
    captions_prompt,
    linkedin_prompt,
    threads_prompt,
)
from src.services.ai.client import AIClient
from src.utils import get_file_name, save_to_file, check_or_create_folder


class ContentGeneratorService:
    """Service for generating content like captions and social media posts"""

    def __init__(self, settings, ai_service: AIClient):
        self.settings = settings
        self.ai_service = ai_service
        self.output_path: str = ""

    def generate_captions(
        self, segments: List, video_path: str, progress_manager: Progress
    ) -> str:
        progress_task = progress_manager.add_task(
            description="[blue]Generating captions...",
            total=1,
        )

        file_name = get_file_name(video_path)

        content_path = os.path.join(
            self.settings.temp_dir, file_name, "content"
        )

        check_or_create_folder(content_path)

        captions_file_path = os.path.join(content_path, "captions.txt")

        # Check if captions file already exists
        if os.path.exists(captions_file_path):
            try:
                with open(captions_file_path, "r", encoding="utf-8") as file:
                    captions_text = file.read()

                    progress_manager.update(
                        progress_task, advance=1, visible=False
                    )

                    return captions_text
            except Exception:
                pass

        captions_text = self._generate_captions(segments)

        save_to_file(captions_file_path, captions_text)

        progress_manager.update(progress_task, advance=1, visible=False)

        return captions_text

    def _generate_captions(self, segments: List) -> str:
        raw_caption = " ".join([seg["text"] for seg in segments])

        response = self.ai_service.request(
            user_prompt=captions_prompt.user_prompt.format(
                raw_caption=raw_caption
            ),
            system_prompt=captions_prompt.system_prompt,
            options=dict(
                temperature=0,
                top_p=0.5,
                frequency_penalty=0.5,
                response_format={"type": "text"},
            ),
        )

        return response

    def generate_linkedin_content(
        self, transcription, progress_manager: Progress
    ):
        """
        Generate LinkedIn content based on transcription

        Args:
            transcription: Transcription text
            progress_manager: Progress manager to track progress

        Returns:
            LinkedIn content
        """
        progress_task = progress_manager.add_task(
            description="[blue]Generating LinkedIn post...",
            total=1,
        )

        response = self.ai_service.request(
            user_prompt=linkedin_prompt.user_prompt.format(
                transcription=transcription
            ),
            system_prompt=linkedin_prompt.system_prompt,
        )

        file_path = os.path.join(self.output_path, "linkedin.txt")
        save_to_file(file_path, response)

        progress_manager.update(progress_task, advance=1, visible=False)

        return response

    def generate_threads_content(
        self, transcription, progress_manager: Progress
    ):
        """
        Generate Threads content based on transcription

        Args:
            transcription: Transcription text

        Returns:
            Threads content
        """
        progress_task = progress_manager.add_task(
            description="[blue]Generating Threads posts...",
            total=1,
        )

        response = self.ai_service.request(
            user_prompt=threads_prompt.user_prompt.format(
                transcription=transcription
            ),
            system_prompt=threads_prompt.system_prompt,
        )

        file_path = os.path.join(self.output_path, "threads.txt")
        save_to_file(file_path, response)

        progress_manager.update(progress_task, advance=1, visible=False)

        return response

    def generate_social_media_content(
        self, video_path: str, captions: str, progress_manager: Progress
    ) -> Tuple[str, str]:
        """
        Generate social media content from captions

        Args:
            video_path: Path to the video file
            captions: Dictionary of captions

        Returns:
            Tuple containing LinkedIn and Threads content
        """
        file_name = get_file_name(video_path)

        self.output_path = os.path.join(self.settings.output_dir, file_name)

        check_or_create_folder(self.output_path)

        linkedin_content = self.generate_linkedin_content(
            captions, progress_manager=progress_manager
        )
        threads_content = self.generate_threads_content(
            captions, progress_manager=progress_manager
        )

        return linkedin_content, threads_content
