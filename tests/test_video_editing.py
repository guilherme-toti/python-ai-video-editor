import pytest
import os
from src.video_editing import edit_video

def test_edit_video():
    video_path = "tests/sample_videos/test_video.mp4"
    segments_to_keep = [{"start": 0, "end": 2, "text": "Test"}]
    output_dir = "tests/output"
    output_path = edit_video(video_path, segments_to_keep, output_dir)
    assert os.path.exists(output_path)
    os.remove(output_path)
