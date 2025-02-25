import pytest
from src.text_analysis import analyze_text

def test_analyze_text():
    transcription = "Hum, vamos começar. Vamos começar de novo."
    segments = [
        {"start": 0, "end": 2, "text": "Hum, vamos começar."},
        {"start": 2, "end": 4, "text": "Vamos começar de novo."}
    ]
    segments_to_keep = analyze_text(transcription, segments)
    assert len(segments_to_keep) == 1
    assert segments_to_keep[0]["text"] == "Vamos começar de novo."
