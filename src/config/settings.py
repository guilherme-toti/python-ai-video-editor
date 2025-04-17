import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings that can be loaded from environment variables"""

    raw_dir: str = os.environ.get("RAW_DIR", "data/raw")
    output_dir: str = os.environ.get("OUTPUT_DIR", "data/output")
    temp_dir: str = os.environ.get("TEMP_DIR", "data/temp")

    video_formats: tuple = (".mp4", ".mov", ".avi", ".mkv")

    is_trello_enabled: bool = False

    def __init__(self):
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

        self.is_trello_enabled = bool(
            os.environ.get("TRELLO_API_KEY") and os.environ.get("TRELLO_TOKEN")
        )
