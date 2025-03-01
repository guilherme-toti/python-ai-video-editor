import json
import os
from typing import List

from rich.progress import Progress

from src.services.ai.client import AIClient
from src.prompts.text_analysis import (
    select_segments_based_on_captions_prompt as captions_prompt,
    generate_select_segments_prompt,
)
from src.utils import get_file_name, read_from_json_file, save_to_file


class TextAnalyzerService:
    """Service for analyzing and refining text content"""

    def __init__(self, settings, ai_service: AIClient):
        self.settings = settings
        self.ai_service = ai_service

    def refine_speech_segments(
        self,
        video_path: str,
        captions: str,
        segments: List,
        progress_manager: Progress,
    ) -> List:
        """
        Analyze and refine text, deciding which segments to keep

        Args:
            video_path: Path to the video file
            captions: Full captions in a string format
            segments: List of speech segments
            progress_manager: Progress manager for updating progress

        Returns:
            List of segments to keep
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        progress_task = progress_manager.add_task(
            description="[blue]Refining speech segments...",
            total=1,
        )

        file_name = get_file_name(video_path)
        refined_speech_segments_path = os.path.join(
            self.settings.temp_dir,
            file_name,
            "audio",
            "refined_speech_segments.json",
        )

        if os.path.exists(refined_speech_segments_path):
            try:
                speech_segments = read_from_json_file(
                    refined_speech_segments_path, expected_type=list
                )

                progress_manager.update(progress_task, advance=1)

                return speech_segments
            except json.decoder.JSONDecodeError:
                pass

        data = {"captions": captions, "segments": segments}

        try:
            response = self.ai_service.request(
                system_prompt=captions_prompt.system_prompt,
                user_prompt=generate_select_segments_prompt(data),
                options=dict(
                    temperature=0.2,
                    response_format={"type": "json_object"},
                ),
            )

            response_obj = json.loads(response)["segments"]

            save_to_file(
                refined_speech_segments_path,
                json.dumps(response_obj, ensure_ascii=False, indent=2),
            )

            progress_manager.update(progress_task, advance=1)

            return response_obj
        except json.JSONDecodeError:
            print("    -> Error: AI response is not valid JSON")

            return segments
        except Exception as e:
            print(f"    -> Error calling OpenAI API: {str(e)}")
            return segments
