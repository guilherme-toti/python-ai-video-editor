import os
from typing import List
from moviepy import VideoFileClip, concatenate_videoclips

from src.utils import get_file_name


class VideoEditorService:
    """Service for editing video based on selected segments"""

    def __init__(self, settings):
        self.settings = settings

    def edit_video(self, video_path: str, segments: List) -> str:
        """
        Edit video to keep only the selected segments
        
        Args:
            video_path: Path to the video file
            segments: List of segments to keep

        Returns:
            Path to the edited video file
        """
        file_name = get_file_name(video_path)
        output_dir = os.path.join(self.settings.output_dir, file_name)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Load the video
        video = VideoFileClip(video_path)

        clips = [video.subclipped(seg["start"], seg["end"]) for seg in segments]

        final_clip = concatenate_videoclips(clips)

        output_path = os.path.join(output_dir, f"edited_{os.path.basename(video_path)}")

        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

        # Clean up
        video.close()
        final_clip.close()

        return output_path
