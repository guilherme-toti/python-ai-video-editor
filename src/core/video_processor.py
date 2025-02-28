import os
from typing import Protocol, List, Union

from rich.progress import TaskID, Progress

from src.utils import get_file_name, check_or_create_folder


class ProgressManager(Protocol):
    def add_task(self, description: str, total_steps: int) -> Union[None, TaskID]: ...

    def update_progress(self, task_id: TaskID, step: int) -> None: ...


class AudioExtractor(Protocol):
    def extract_audio(self, video_path: str) -> str: ...

    def extract_raw_segments(self, audio_path: str) -> List: ...


class Transcriber(Protocol):
    def transcribe(self, audio_path: str, speech_segments: List) -> List: ...


class TextAnalyzer(Protocol):
    def refine_speech_segments(self, video_path: str, captions: str, segments: List) -> List: ...


class VideoEditor(Protocol):
    def edit_video(self, video_path: str, segments: List) -> str: ...


class ContentGenerator(Protocol):
    def generate_captions(self, segments: List, video_path: str) -> str: ...

    def generate_social_media_content(self, video_path: str, captions: str) -> tuple: ...


STEPS = "7"


class VideoProcessor:
    def __init__(
            self,
            audio_extractor: AudioExtractor,
            transcriber: Transcriber,
            text_analyzer: TextAnalyzer,
            video_editor: VideoEditor,
            content_generator: ContentGenerator,
            progress_manager: ProgressManager,
            settings=None,
    ):
        self.audio_extractor = audio_extractor
        self.transcriber = transcriber
        self.text_analyzer = text_analyzer
        self.video_editor = video_editor
        self.content_generator = content_generator
        self.progress_manager = progress_manager
        self.settings = settings

    def create_temp_folder(self, video_path: str):
        file_name = get_file_name(video_path)
        folder_path = os.path.join(self.settings.temp_dir, file_name)

        check_or_create_folder(folder_path)

    def process_video(self, video_path: str):
        """
        Process a single video and generate outputs.
        
        Args:
            video_path (str): Path to the video file.

        Returns:
            dict: Results including paths to generated files and content
        """
        print(f"Starting to process video: {video_path}")

        try:
            self.create_temp_folder(video_path)

            print(f"[1/{STEPS}] Extracting audio from video...")
            audio_path = self.audio_extractor.extract_audio(video_path=video_path)

            print(f"[2/{STEPS}] Extracting raw speech segments...")
            speech_segments = self.audio_extractor.extract_raw_segments(audio_path)

            print(f"[3/{STEPS}] Transcribing speech segments...")
            transcribed_speech_segments = self.transcriber.transcribe(audio_path, speech_segments)

            print(f"[4/{STEPS}] Generating captions...")
            captions = self.content_generator.generate_captions(
                video_path=video_path,
                segments=transcribed_speech_segments
            )

            print(f"[5/{STEPS}] Refining speech segments...")
            refined_speech_segments = self.text_analyzer.refine_speech_segments(
                video_path=video_path,
                captions=captions,
                segments=transcribed_speech_segments
            )

            print(f"[6/{STEPS}] Editing video...")
            self.video_editor.edit_video(video_path, refined_speech_segments)

            print(f"[7/{STEPS}] Generating social media content...")
            self.content_generator.generate_social_media_content(
                video_path=video_path,
                captions=captions,
            )
        except Exception as e:
            import traceback
            print(f"Error in video processing: {str(e)}")
            print(traceback.format_exc())
            raise
