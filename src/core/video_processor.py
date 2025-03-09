import os
from concurrent.futures import ThreadPoolExecutor

from src.core.progress_manager import progress_object
from src.core.protocols import (
    AudioExtractor,
    Transcriber,
    TextAnalyzer,
    VideoEditor,
    ContentGenerator,
)
from src.services.third_party.trello import Trello
from src.utils import get_file_name, check_or_create_folder


class VideoProcessor:
    def __init__(
        self,
        audio_extractor: AudioExtractor,
        transcriber: Transcriber,
        text_analyzer: TextAnalyzer,
        video_editor: VideoEditor,
        content_generator: ContentGenerator,
        settings=None,
    ):
        # Initialize components
        self.audio_extractor = audio_extractor
        self.transcriber = transcriber
        self.text_analyzer = text_analyzer
        self.video_editor = video_editor
        self.content_generator = content_generator
        self.trello = Trello()
        self.settings = settings

    def create_temp_folder(self, video_path: str):
        file_name = get_file_name(video_path)
        folder_path = os.path.join(self.settings.temp_dir, file_name)

        check_or_create_folder(folder_path)

    def delete_temp_folder(self, video_path: str):
        file_name = get_file_name(video_path)
        folder_path = os.path.join(self.settings.temp_dir, file_name)

        os.system(f"rm -r {folder_path}")

    def process_video(self, video_path: str):
        """
        Process a single video and generate outputs.

        Args:
            video_path (str): Path to the video file.

        Returns:
            dict: Results including paths to generated files and content
        """
        file_name = get_file_name(video_path)

        with progress_object as progress_manager:
            try:
                print(f"Processing video: {file_name}")

                self.create_temp_folder(video_path)

                audio_path = self.audio_extractor.extract_audio(
                    video_path=video_path,
                )

                speech_segments = self.audio_extractor.extract_raw_segments(
                    audio_path,
                )

                transcribed_speech_segments = self.transcriber.transcribe(
                    audio_path=audio_path,
                    speech_segments=speech_segments,
                )

                captions = self.content_generator.generate_captions(
                    video_path=video_path,
                    segments=transcribed_speech_segments,
                )

                refined_speech_segments = (
                    self.text_analyzer.refine_speech_segments(
                        video_path=video_path,
                        captions=captions,
                        segments=transcribed_speech_segments,
                    )
                )

                if not refined_speech_segments:
                    error_message = (
                        f"Video {file_name} failed to create"
                        " refined speech segments 🚫"
                    )

                    print(error_message)

                    return

                self.video_editor.edit_video(
                    video_path,
                    refined_speech_segments,
                    progress_manager=progress_manager,
                )

                linkedin_content, threads_content = (
                    self.content_generator.generate_social_media_content(
                        video_path=video_path,
                        captions=captions,
                    )
                )

                with ThreadPoolExecutor() as executor:
                    linkedin_comment = executor.submit(
                        self.trello.add_comment,
                        file_name,
                        f"**LinkedIn Post:**\n```{linkedin_content}```",
                    )
                    threads_comment = executor.submit(
                        self.trello.add_comment,
                        file_name,
                        f"**Threads Post:**\n```{threads_content}```",
                    )

                    linkedin_comment.result()
                    threads_comment.result()

                # self.delete_temp_folder(video_path)

                print(f"Video {file_name} completed ✅")
            except Exception as e:
                import traceback

                print(f"Error in video processing: {str(e)}")
                print(traceback.format_exc())
                raise
