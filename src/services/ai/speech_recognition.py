from concurrent.futures import ThreadPoolExecutor
from typing import List
import warnings

import torch
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
            model_id,
            torch_dtype=torch_dtype,
            use_safetensors=True,
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

    def get_audio_transcription(self, audio_path: str) -> dict:
        try:
            response = self.whisper_pipeline(
                audio_path,
                batch_size=1,
                generate_kwargs={
                    "language": "portuguese",
                    "task": "transcribe",
                    "temperature": 0.0,
                },
            )

            return response
        except Exception as e:
            print(f"Error transcribing segment: {audio_path}. Error: {e}")

            return {"text": ""}

    def transcribe(self, audio_segments_path: List) -> List:
        with ThreadPoolExecutor() as executor:
            results = list(
                executor.map(
                    self.get_audio_transcription,
                    audio_segments_path,
                )
            )

        return results
