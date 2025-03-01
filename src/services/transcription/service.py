import json
import os
import subprocess
from typing import List

from rich.progress import Progress

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
        progress_manager: Progress,
    ) -> List:
        """
        Transcribe speech segments from audio

        Args:
            audio_path: Path to the audio file
            speech_segments: list containing speech segments
            progress_manager: Progress manager instance

        Returns:
            List containing the full transcription text and segments
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        generate_audio_task = progress_manager.add_task(
            description="[green]Generating transcription audio files...",
            start=False,
        )

        file_name = get_file_name(audio_path)

        temp_audio_path = os.path.join(
            self.settings.temp_dir, file_name, "audio"
        )

        speech_segments_file_path = os.path.join(
            temp_audio_path, "speech_segments.json"
        )

        if os.path.exists(speech_segments_file_path):
            progress_manager.update(generate_audio_task, total=1)
            progress_manager.start_task(generate_audio_task)

            try:
                speech_segments = read_from_json_file(
                    file_path=speech_segments_file_path, expected_type=list
                )

                progress_manager.update(
                    generate_audio_task, completed=1, visible=False
                )

                return speech_segments
            except json.decoder.JSONDecodeError:
                progress_manager.reset(generate_audio_task)
                pass

        self.folder_path = os.path.join(temp_audio_path, "segments")

        check_or_create_folder(self.folder_path)

        transcribed_segments = []

        if self.speech_recognition_service is None:
            self.speech_recognition_service = SpeechRecognition()

        # Process each speech segment
        total_segments = len(speech_segments)
        audio_segments_path = []

        progress_manager.update(generate_audio_task, total=total_segments)
        progress_manager.start_task(generate_audio_task)

        for i, segment in enumerate(speech_segments):
            start_time = segment["start"]
            end_time = segment["end"]

            # Define segment path
            segment_path = os.path.join(self.folder_path, f"{i}.mp3")
            audio_segments_path.append(segment_path)

            # Check if segment file already exists
            if os.path.exists(segment_path):
                progress_manager.update(generate_audio_task, advance=1)
            else:
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

                progress_manager.update(generate_audio_task, advance=1)

        # Transcribe the segments
        transcription = self.speech_recognition_service.transcribe(
            audio_segments_path,
            progress_manager=progress_manager,
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

        progress_manager.update(generate_audio_task, visible=False)

        return transcribed_segments
