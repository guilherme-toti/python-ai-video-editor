import json
import os
import torch
from typing import List
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from moviepy import AudioFileClip

from src.utils import get_file_name, check_or_create_folder, save_to_file, read_from_json_file


class TranscriptionService:
    """Service for transcribing audio segments"""

    def __init__(self, settings):
        self.settings = settings
        self.folder_path: str = ""

        # Initialize Whisper model
        self.INITIAL_PROMPT = "Eu falo sobre tecnologia, programação e trabalho remoto. Meu nicho principal é ajudar desenvolvedores de software a conquistar seu primeiro trabalho remoto para o exterior."

        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = "openai/whisper-large-v3"

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            use_safetensors=True
        )
        self.model.to(device)

        self.processor = AutoProcessor.from_pretrained(model_id)

        self.whisper_pipeline = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
            model_kwargs={"use_cache": True}
        )

    def transcribe_audio_segment(self, segment_audio_path: str) -> dict:
        """
        Transcribe an audio segment using the Whisper model
        
        Args:
            segment_audio_path: Path to the audio segment
            
        Returns:
            Dictionary with transcription results
        """
        try:
            response = self.whisper_pipeline(
                segment_audio_path,
                batch_size=1,
                generate_kwargs={"language": "portuguese", "task": "transcribe"},
            )

            return response
        except Exception as e:
            print(f"Error transcribing segment: {e}")
            return {"text": ""}

    def transcribe(self, audio_path: str, speech_segments: List) -> List:
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

        file_name = get_file_name(audio_path)

        temp_audio_path = os.path.join(self.settings.temp_dir, file_name, "audio")

        speech_segments_file_path = os.path.join(temp_audio_path, "speech_segments.json")

        if os.path.exists(speech_segments_file_path):
            try:
                speech_segments = read_from_json_file(file_path=speech_segments_file_path, expected_type=list)

                print(f"    -> Using previously transcribed speech segments.")

                return speech_segments
            except json.decoder.JSONDecodeError:
                print(f"    -> Error reading transcribed speech segments from file. Reprocessing...")

        self.folder_path = os.path.join(temp_audio_path, "segments")

        # Load the audio file
        audio_clip = AudioFileClip(audio_path)

        transcribed_segments = []

        check_or_create_folder(self.folder_path)

        # Process each speech segment
        total_segments = len(speech_segments)
        for i, segment in enumerate(speech_segments):
            start_time = segment["start"]
            end_time = segment["end"]

            # Define segment path
            segment_path = os.path.join(self.folder_path, f"{i}.mp3")
            segment_text = None

            # Check if segment file already exists
            if os.path.exists(segment_path):
                try:
                    # Transcribe the existing segment
                    result = self.transcribe_audio_segment(segment_path)
                    segment_text = result["text"].strip()
                    print(f"    -> Using existing segment file: {i}/{total_segments}...")
                except Exception as e:
                    print(f"    !! Error using existing segment: {e}")
                    segment_text = None

            # If segment doesn't exist or transcription failed, create it
            if segment_text is None:
                # Extract the segment audio
                print(f"    -> Transcribing segment {i}/{total_segments}...")
                segment_audio = audio_clip.subclipped(start_time, end_time)
                segment_audio.write_audiofile(segment_path)

                # Transcribe the segment
                result = self.transcribe_audio_segment(segment_path)
                segment_text = result["text"].strip()

            # Add to results
            if segment_text:  # Only add if there's actual transcribed text
                transcribed_segment = {
                    "start": start_time,
                    "end": end_time,
                    "text": segment_text
                }
                transcribed_segments.append(transcribed_segment)

        audio_clip.close()

        save_to_file(speech_segments_file_path, json.dumps(transcribed_segments, ensure_ascii=False, indent=2))

        return transcribed_segments
