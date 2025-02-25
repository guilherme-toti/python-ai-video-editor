import os
from transcription import transcribe_video
from text_analysis import analyze_text
from video_editing import edit_video
from text_generation import generate_captions, generate_social_media_content

def process_video(video_path, output_dir):
    """
    Process a single video and generate outputs.
    
    Args:
        video_path (str): Path to the video file.
        output_dir (str): Directory to save outputs.
    """
    # Transcribe video
    transcription, segments = transcribe_video(video_path)
    
    # Analyze text
    segments_to_keep = analyze_text(transcription, segments)
    
    # Edit video
    final_video_path = edit_video(video_path, segments_to_keep, output_dir)
    
    # Generate captions
    captions = generate_captions(segments_to_keep)
    captions_path = os.path.join(output_dir, f"captions_{os.path.basename(video_path)}.txt")
    with open(captions_path, "w", encoding="utf-8") as f:
        f.write(captions)
    
    # Generate social media content
    linkedin_content, threads_content = generate_social_media_content(transcription)
    social_media_path = os.path.join(output_dir, f"social_media_{os.path.basename(video_path)}.txt")
    with open(social_media_path, "w", encoding="utf-8") as f:
        f.write(f"LinkedIn:\n{linkedin_content}\n\nThreads:\n{threads_content}")

if __name__ == "__main__":
    raw_dir = "raw"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    for video_file in os.listdir(raw_dir):
        video_path = os.path.join(raw_dir, video_file)
        process_video(video_path, output_dir)
