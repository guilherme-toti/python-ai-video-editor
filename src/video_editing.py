from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def edit_video(video_path, segments_to_keep, output_dir):
    """
    Edit video to keep specified segments and render to output directory.
    
    Args:
        video_path (str): Path to the original video.
        segments_to_keep (list): List of segments with start and end times.
        output_dir (str): Directory to save the edited video.
    
    Returns:
        str: Path to the edited video.
    """
    os.makedirs(output_dir, exist_ok=True)
    video = VideoFileClip(video_path)
    clips = [video.subclip(seg["start"], seg["end"]) for seg in segments_to_keep]
    final_clip = concatenate_videoclips(clips)
    output_path = os.path.join(output_dir, f"edited_{os.path.basename(video_path)}")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    video.close()
    final_clip.close()
    return output_path
