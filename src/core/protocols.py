from typing import Protocol, List

from rich.progress import Progress


class AudioExtractor(Protocol):
    def extract_audio(self, video_path: str) -> str: ...

    def extract_raw_segments(self, audio_path: str) -> List: ...


class Transcriber(Protocol):
    def transcribe(
        self,
        audio_path: str,
        speech_segments: List,
    ) -> List: ...


class TextAnalyzer(Protocol):
    def refine_speech_segments(
        self,
        video_path: str,
        captions: str,
        segments: List,
    ) -> List: ...


class VideoEditor(Protocol):
    def edit_video(
        self, video_path: str, segments: List, progress_manager: Progress
    ) -> None: ...


class ContentGenerator(Protocol):
    def generate_captions(self, segments: List, video_path: str) -> str: ...

    def generate_social_media_content(
        self, video_path: str, captions: str
    ) -> tuple: ...
