import os
import subprocess
from typing import List

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

        output_path = os.path.join(
            output_dir, f"edited_{os.path.basename(video_path)}"
        )

        # Create a temporary file for the ffmpeg filter complex script
        temp_filter_path = os.path.join(output_dir, "filter_script.txt")

        # Build the filter complex for trimming and concatenating segments
        filter_parts = []
        segment_parts = []

        for i, seg in enumerate(segments):
            # Add a segment trim filter
            filter_parts.append(
                f"[0:v]trim=start={seg['start']}:end={seg['end']},"
                f"setpts=PTS-STARTPTS[v{i}];"
            )
            filter_parts.append(
                f"[0:a]atrim=start={seg['start']}:end={seg['end']},"
                f"asetpts=PTS-STARTPTS[a{i}];"
            )
            segment_parts.append(f"[v{i}][a{i}]")

        # Concatenate segments
        filter_parts.append(
            f"{' '.join(segment_parts)}concat=n={len(segments)}:"
            f"v=1:a=1[outv][outa]"
        )

        # Write filter complex to file
        with open(temp_filter_path, "w") as f:
            f.write("".join(filter_parts))

        # Build and execute ffmpeg command
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            video_path,
            "-filter_complex_script",
            temp_filter_path,
            "-map",
            "[outv]",
            "-map",
            "[outa]",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-loglevel",
            "quiet",
            output_path,
        ]

        subprocess.run(ffmpeg_cmd, check=True)

        # Clean up the temporary filter script
        if os.path.exists(temp_filter_path):
            os.remove(temp_filter_path)

        return output_path
