import os
from typing import Protocol, List

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TaskProgressColumn,
    BarColumn,
)
from rich.text import Text

from src.utils import get_file_name, check_or_create_folder


class AudioExtractor(Protocol):
    def extract_audio(
        self, video_path: str, progress_manager: Progress
    ) -> str: ...

    def extract_raw_segments(
        self, audio_path: str, progress_manager: Progress
    ) -> List: ...


class Transcriber(Protocol):
    def transcribe(
        self,
        audio_path: str,
        speech_segments: List,
        progress_manager: Progress,
    ) -> List: ...


class TextAnalyzer(Protocol):
    def refine_speech_segments(
        self,
        video_path: str,
        captions: str,
        segments: List,
        progress_manager: Progress,
    ) -> List: ...


class VideoEditor(Protocol):
    def edit_video(
        self, video_path: str, segments: List, progress_manager: Progress
    ) -> None: ...


class ContentGenerator(Protocol):
    def generate_captions(
        self, segments: List, video_path: str, progress_manager: Progress
    ) -> str: ...

    def generate_social_media_content(
        self, video_path: str, captions: str, progress_manager: Progress
    ) -> tuple: ...


STEPS = "7"

progress = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
)


class VideoProcessor:
    def __init__(
        self,
        audio_extractor: AudioExtractor,
        transcriber: Transcriber,
        text_analyzer: TextAnalyzer,
        video_editor: VideoEditor,
        content_generator: ContentGenerator,
        settings=None,
    ):
        # Initialize components
        self.audio_extractor = audio_extractor
        self.transcriber = transcriber
        self.text_analyzer = text_analyzer
        self.video_editor = video_editor
        self.content_generator = content_generator
        self.settings = settings

    def create_temp_folder(self, video_path: str):
        file_name = get_file_name(video_path)
        folder_path = os.path.join(self.settings.temp_dir, file_name)

        check_or_create_folder(folder_path)

    def delete_temp_folder(self, video_path: str):
        file_name = get_file_name(video_path)
        folder_path = os.path.join(self.settings.temp_dir, file_name)

        os.system(f"rm -r {folder_path}")

    def process_video(self, video_path: str):
        """
        Process a single video and generate outputs.

        Args:
            video_path (str): Path to the video file.

        Returns:
            dict: Results including paths to generated files and content
        """
        console = Console()
        text = Text(f"Processing video: {video_path}")
        text.stylize("bold green")
        console.print(text)

        with progress as progress_manager:
            try:
                self.create_temp_folder(video_path)

                audio_path = self.audio_extractor.extract_audio(
                    video_path=video_path,
                    progress_manager=progress_manager,
                )

                speech_segments = self.audio_extractor.extract_raw_segments(
                    audio_path,
                    progress_manager=progress_manager,
                )

                transcribed_speech_segments = self.transcriber.transcribe(
                    audio_path=audio_path,
                    speech_segments=speech_segments,
                    progress_manager=progress_manager,
                )

                captions = self.content_generator.generate_captions(
                    video_path=video_path,
                    segments=transcribed_speech_segments,
                    progress_manager=progress_manager,
                )

                refined_speech_segments = (
                    self.text_analyzer.refine_speech_segments(
                        video_path=video_path,
                        captions=captions,
                        segments=transcribed_speech_segments,
                        progress_manager=progress_manager,
                    )
                )

                self.video_editor.edit_video(
                    video_path,
                    refined_speech_segments,
                    progress_manager=progress_manager,
                )

                self.content_generator.generate_social_media_content(
                    video_path=video_path,
                    captions=captions,
                    progress_manager=progress_manager,
                )

                self.delete_temp_folder(video_path)
            except Exception as e:
                import traceback

                print(f"Error in video processing: {str(e)}")
                print(traceback.format_exc())
                raise

        os.system('cls' if os.name == 'nt' else 'clear')

        text = Text(f"Finished processing: {video_path} ✅")
        text.stylize("bold green")
        console.print(text)
