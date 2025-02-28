import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

INITIAL_PROMPT = (
    "Eu falo sobre tecnologia, programação e trabalho remoto. "
    "Meu nicho principal é ajudar desenvolvedores de software a"
    " conquistar seu primeiro trabalho remoto para o exterior."
)


class SpeechRecognition:
    def __init__(self):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = (
            torch.float16 if torch.cuda.is_available() else torch.float32
        )

        model_id = "openai/whisper-large-v3"

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, use_safetensors=True
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
            model_kwargs={"use_cache": True},
        )

    def transcribe(self, audio_path: str) -> dict:
        try:
            response = self.whisper_pipeline(
                audio_path,
                batch_size=1,
                generate_kwargs={
                    "language": "portuguese",
                    "task": "transcribe",
                },
            )

            return response
        except Exception as e:
            print(f"Error transcribing segment: {e}")
            return {"text": ""}
