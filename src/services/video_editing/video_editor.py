import os
import re
import subprocess
from typing import List

from rich.progress import Progress

from src.utils import get_file_name


class VideoEditorService:
    """Service for editing video based on selected segments"""

    def __init__(self, settings):
        self.settings = settings

    @staticmethod
    def get_segments_duration(segments: List) -> float:
        """Calculate the total duration of the segments."""
        return float(sum(seg["end"] - seg["start"] for seg in segments))

    def edit_video(
        self, video_path: str, segments: List, progress_manager: Progress
    ) -> None:
        """
        Edit video to keep only the selected segments

        Args:
            video_path: Path to the video file
            segments: List of segments to keep
            progress_manager: Progress manager for updating progress

        Returns:
            Path to the edited video file
        """
        total_duration = self.get_segments_duration(segments)

        if total_duration is None:
            print("Could not determine video duration.")
            return

        progress_task = progress_manager.add_task(
            description="[red]Editing video...",
            total=total_duration,
        )

        print("    -> Editing video...")

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
            "-crf",
            "12",
            "-preset",
            "slow",
            "-c:a",
            "aac",
            "-b:a",
            "320k",
            output_path,
        ]

        time_pattern = re.compile(r'time=(\d+:\d+:\d+\.\d+)')

        def time_to_seconds(time_str):
            """Convert hh:mm:ss.ms to seconds."""
            h, m, s = map(float, time_str.split(":"))
            return h * 3600 + m * 60 + s

        process = subprocess.Popen(
            ffmpeg_cmd,
            stderr=subprocess.PIPE,
            text=True,
            universal_newlines=True,
            bufsize=1,
        )

        for line in process.stderr:
            match = time_pattern.search(line)
            if match:
                current_time = time_to_seconds(match.group(1))
                progress_manager.update(progress_task, completed=current_time)

        process.wait()

        # Clean up the temporary filter script
        if os.path.exists(temp_filter_path):
            os.remove(temp_filter_path)

        progress_manager.update(
            progress_task, completed=total_duration, visible=False
        )

        print("      -> Video edited.")
