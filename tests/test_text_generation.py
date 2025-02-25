import pytest
from src.text_generation import generate_captions, generate_social_media_content

def test_generate_captions():
    segments_to_keep = [{"start": 0, "end": 2, "text": "Test caption"}]
    captions = generate_captions(segments_to_keep)
    assert captions == "Test caption"

def test_generate_social_media_content():
    transcription = "Este é um teste."
    linkedin_content, threads_content = generate_social_media_content(transcription)
    assert isinstance(linkedin_content, str)
    assert isinstance(threads_content, str)
    assert len(linkedin_content) > 0
    assert len(threads_content) > 0
