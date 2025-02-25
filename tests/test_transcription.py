import pytest
from src.transcription import transcribe_video

def test_transcribe_video():
    video_path = "tests/sample_videos/test_video.mp4"
    transcription, segments = transcribe_video(video_path)
    assert isinstance(transcription, str)
    assert len(segments) > 0
    assert "start" in segments[0]
    assert "end" in segments[0]
    assert "text" in segments[0]

def test_transcribe_video_not_found():
    with pytest.raises(FileNotFoundError):
        transcribe_video("nonexistent.mp4")
