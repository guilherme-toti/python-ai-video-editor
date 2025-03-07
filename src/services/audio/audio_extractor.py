import os
import json
import subprocess
from typing import List

import torchaudio
import torch

from src.utils import (
    get_file_name,
    check_or_create_folder,
    save_to_file,
    read_from_json_file,
)


class AudioExtractorService:
    """Service for extracting audio and speech segments from video files"""

    def __init__(self, settings):
        self.settings = settings
        self.file_name: str = ""
        self.folder_path: str = ""
        self.gap_threshold: float = 1.0
        self.max_segment_length: float = 5.0

        # Load Silero VAD model
        self.model, utils = torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
            force_reload=True,
        )
        (
            self.get_speech_timestamps,
            self.save_audio,
            self.read_audio,
            _,
            _,
        ) = utils

    def extract_audio(self, video_path: str) -> str:
        """
        Extract audio from a video file using ffmpeg

        Args:
            video_path: Path to the video file

        Returns:
            Path to the extracted audio file
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        print("    -> Extracting audio...")

        self.file_name = get_file_name(video_path)
        self.folder_path = os.path.join(
            self.settings.temp_dir, self.file_name, "audio"
        )

        audio_filename = self.file_name + ".mp3"
        audio_path = os.path.join(self.folder_path, audio_filename)

        # Check if audio has already been extracted
        if os.path.exists(audio_path):
            print("      -> Audio already extracted - using cached version.")

            return audio_path

        check_or_create_folder(self.folder_path)

        # Extract audio from video using ffmpeg
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            video_path,
            "-vn",  # No video
            "-acodec",
            "libmp3lame",  # MP3 codec
            "-q:a",
            "2",  # Quality setting
            "-loglevel",
            "quiet",  # Suppress logs
            audio_path,
        ]

        subprocess.run(ffmpeg_cmd, check=True)
        print("      -> Audio extracted successfully.")

        return audio_path

    def extract_raw_segments(self, audio_path: str) -> List:
        """
        Extract speech segments from an audio file

        Args:
            audio_path: Path to the audio file

        Returns:
            JSON string containing speech segments
        """
        print("    -> Extracting raw segments...")

        raw_speech_segments_file_path = os.path.join(
            self.folder_path, "raw_speech_segments.json"
        )

        if os.path.exists(raw_speech_segments_file_path):
            try:
                speech_segments = read_from_json_file(
                    raw_speech_segments_file_path, expected_type=list
                )

                message = (
                    "      -> Raw speech segments already extracted - "
                    "using cached version."
                )

                print(message)

                return speech_segments
            except json.decoder.JSONDecodeError:
                pass

        # Load audio using torchaudio
        wav, sr = torchaudio.load(audio_path)

        # Convert to mono if stereo
        if wav.shape[0] > 1:
            wav = torch.mean(wav, dim=0)

        # Resample to 16kHz if needed
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(sr, 16000)
            wav = resampler(wav)

        # Get speech timestamps
        speech_timestamps = self.get_speech_timestamps(
            wav, self.model, sampling_rate=16000
        )

        segments = []
        for ts in speech_timestamps:
            start_sec = ts["start"] / 16000  # Convert from samples to seconds
            end_sec = ts["end"] / 16000  # Convert from samples to seconds
            segments.append({"start": start_sec, "end": end_sec})

        combined_segments = []
        current_segment = None

        for seg in segments:
            if not current_segment:
                # If there's no "active" segment to merge into, start a new one
                current_segment = seg
            else:
                gap = seg["start"] - current_segment["end"]
                merged_length = seg["end"] - current_segment["start"]

                # If gap is small enough AND the merged length won't
                # exceed the limit, merge
                if (
                    gap < self.gap_threshold
                    and merged_length <= self.max_segment_length
                ):
                    # Extend the current segment to the new end time
                    current_segment["end"] = seg["end"]
                else:
                    # Otherwise, push the old one and start a new segment
                    combined_segments.append(current_segment)
                    current_segment = seg

        # Append the last segment if it exists
        if current_segment:
            combined_segments.append(current_segment)

        save_to_file(
            raw_speech_segments_file_path,
            json.dumps(combined_segments, ensure_ascii=False, indent=2),
        )

        print("      -> Raw speech segments extracted successfully.")

        return combined_segments
