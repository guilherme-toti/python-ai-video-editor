import sys
import os
import traceback
from dotenv import load_dotenv

from src.config.settings import Settings
from src.core.video_processor import VideoProcessor
from src.services.ai.openai import OpenAI
from src.services.audio.audio_extractor import AudioExtractorService
from src.services.transcription.transcriber import TranscriptionService
from src.services.text_analysis.text_analyzer import TextAnalyzerService
from src.services.video_editing.video_editor import VideoEditorService
from src.services.content.content_generator import ContentGeneratorService


load_dotenv()


def main():
    sys.stderr = open(os.devnull, "w")

    # Load settings
    settings = Settings()

    # Create service instances
    ai_service = OpenAI()
    audio_extractor = AudioExtractorService(settings)
    transcriber = TranscriptionService(settings)
    text_analyzer = TextAnalyzerService(
        settings=settings, ai_service=ai_service
    )
    video_editor = VideoEditorService(settings)
    content_generator = ContentGeneratorService(
        settings=settings, ai_service=ai_service
    )

    # Create the video processor with all dependencies
    processor = VideoProcessor(
        audio_extractor=audio_extractor,
        transcriber=transcriber,
        text_analyzer=text_analyzer,
        video_editor=video_editor,
        content_generator=content_generator,
        settings=settings,
    )

    # Process all videos
    for video_file in os.listdir(settings.raw_dir):
        if not video_file.lower().endswith(settings.video_formats):
            print("There is no video file to process.")
            continue

        video_path = os.path.join(settings.raw_dir, video_file)
        try:
            processor.process_video(video_path)
        except Exception as e:
            traceback.print_exc()
            print(f"Error processing {video_file}: {str(e)}")


if __name__ == "__main__":
    main()
