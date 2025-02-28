import os
import traceback

from src.config.settings import Settings
from src.core.progress_manager import ProgressManager
from src.core.video_processor import VideoProcessor
from src.services.ai.openai import OpenAI
from src.services.audio.extractor import AudioExtractorService
from src.services.transcription.service import TranscriptionService
from src.services.text_analysis.analyzer import TextAnalyzerService
from src.services.video_editing.editor import VideoEditorService
from src.services.content.generator import ContentGeneratorService


def main():
    # Load settings
    settings = Settings()

    # Create service instances
    ai_service = OpenAI()
    audio_extractor = AudioExtractorService(settings)
    transcriber = TranscriptionService(settings)
    text_analyzer = TextAnalyzerService(settings=settings, ai_service=ai_service)
    video_editor = VideoEditorService(settings)
    content_generator = ContentGeneratorService(settings=settings, ai_service=ai_service)
    progress_manager = ProgressManager()

    # Create the video processor with all dependencies
    processor = VideoProcessor(
        audio_extractor=audio_extractor,
        transcriber=transcriber,
        text_analyzer=text_analyzer,
        video_editor=video_editor,
        content_generator=content_generator,
        settings=settings,
        progress_manager=progress_manager
    )

    # Process all videos
    for video_file in os.listdir(settings.raw_dir):
        if not video_file.lower().endswith(settings.video_formats):
            continue

        video_path = os.path.join(settings.raw_dir, video_file)
        try:
            processor.process_video(video_path)
            print(f"Successfully processed {video_file}")
        except Exception as e:
            traceback.print_exc()
            print(f"Error processing {video_file}: {str(e)}")


if __name__ == "__main__":
    main()
