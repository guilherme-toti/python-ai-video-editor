import json
import os
import subprocess
from typing import List

from src.services.ai.speech_recognition import SpeechRecognition
from src.utils import (
    get_file_name,
    check_or_create_folder,
    save_to_file,
    read_from_json_file,
)


class TranscriptionService:
    """Service for transcribing audio segments"""

    def __init__(self, settings):
        self.settings = settings
        self.folder_path: str = ""
        self.speech_recognition_service = None

    def transcribe(
        self,
        audio_path: str,
        speech_segments: List,
    ) -> List:
        """
        Transcribe speech segments from audio

        Args:
            audio_path: Path to the audio file
            speech_segments: list containing speech segments

        Returns:
            List containing the full transcription text and segments
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print("    -> Generating transcription audio files...")

        file_name = get_file_name(audio_path)

        temp_audio_path = os.path.join(
            self.settings.temp_dir, file_name, "audio"
        )

        speech_segments_file_path = os.path.join(
            temp_audio_path, "speech_segments.json"
        )

        if os.path.exists(speech_segments_file_path):
            try:
                speech_segments = read_from_json_file(
                    file_path=speech_segments_file_path, expected_type=list
                )

                message = (
                    "      -> Transcription already generated - "
                    "using cached version."
                )

                print(message)

                return speech_segments
            except json.decoder.JSONDecodeError:
                pass

        self.folder_path = os.path.join(temp_audio_path, "segments")

        check_or_create_folder(self.folder_path)

        transcribed_segments = []

        if self.speech_recognition_service is None:
            self.speech_recognition_service = SpeechRecognition()

        # Process each speech segment
        audio_segments_path = []

        for i, segment in enumerate(speech_segments):
            start_time = segment["start"]
            end_time = segment["end"]

            # Define segment path
            segment_path = os.path.join(self.folder_path, f"{i}.mp3")
            audio_segments_path.append(segment_path)

            # Check if segment file already exists
            if not os.path.exists(segment_path):
                # Extract the segment audio using ffmpeg
                # Calculate duration in seconds
                duration = end_time - start_time

                # Use ffmpeg to extract the segment
                ffmpeg_cmd = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    audio_path,
                    "-ss",
                    str(start_time),
                    "-t",
                    str(duration),
                    "-acodec",
                    "libmp3lame",
                    "-q:a",
                    "2",
                    "-loglevel",
                    "quiet",
                    segment_path,
                ]

                subprocess.run(ffmpeg_cmd, check=True)

        # Transcribe the segments
        transcription = self.speech_recognition_service.transcribe(
            audio_segments_path,
        )

        if not len(transcription) == len(speech_segments):
            raise ValueError(
                "Transcription length does not match speech segments length."
            )

        for i, segment in enumerate(speech_segments):
            start_time = segment["start"]
            end_time = segment["end"]

            # Get the transcription result
            result = transcription[i]
            segment_text = result["text"].strip()

            # Add to results
            if not segment_text:
                continue

            transcribed_segment = {
                "start": start_time,
                "end": end_time,
                "text": segment_text,
            }

            transcribed_segments.append(transcribed_segment)

        save_to_file(
            speech_segments_file_path,
            json.dumps(transcribed_segments, ensure_ascii=False, indent=2),
        )

        print("      -> Transcription completed.")
        return transcribed_segments
