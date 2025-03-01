from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import List
import warnings

import torch
from rich.progress import Progress
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

warnings.filterwarnings("ignore", category=FutureWarning)


class SpeechRecognition:
    def __init__(self):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = (
            torch.float16 if torch.cuda.is_available() else torch.float32
        )

        model_id = "openai/whisper-large-v3"

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, use_safetensors=True
        ).to(device)

        self.processor = AutoProcessor.from_pretrained(model_id)

        self.whisper_pipeline = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
            model_kwargs={"use_cache": True},
        )

    def get_audio_transcription(
        self, audio_path: str, update_progress
    ) -> dict:
        try:
            response = self.whisper_pipeline(
                audio_path,
                batch_size=1,
                generate_kwargs={
                    "language": "portuguese",
                    "task": "transcribe",
                },
            )

            update_progress()

            return response
        except Exception as e:
            print(f"Error transcribing segment: {audio_path}. Error: {e}")

            update_progress()

            return {"text": ""}

    def transcribe(
        self, audio_segments_path: List, progress_manager: Progress
    ) -> List:
        transcribe_audio_task = progress_manager.add_task(
            description="[green]Transcribing speech segments...",
            total=len(audio_segments_path),
        )

        def update_progress():
            progress_manager.update(transcribe_audio_task, advance=1)

        with ThreadPoolExecutor() as executor:
            executor_function = partial(
                self.get_audio_transcription, update_progress=update_progress
            )

            results = list(
                executor.map(
                    executor_function,
                    audio_segments_path,
                )
            )

        return results
