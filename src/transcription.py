import subprocess
from moviepy.editor import VideoFileClip

def extract_AUDIO(vid_path, audio_path):
    video = VideoFileClip(vid_path)
    video.audio.writeAudiofile(audio_path)
    video.close()

def run_whisper_cpp(audio_path, output_path):
    cmd = f"./bin/whisper -f {audio_path} -t -o {output_path}"
    subprocess.run(cmd, shell=True)

def parse_whisper_output(output_path):
    with open(output_path, 'r') as f:
        lines = f.readlines()
    
    word_list = []
    for line in lines:
        word, start, end = line.strip().split()
        word_list.append((word, float(start), float(end)))
    
    sentences = []
    current_sentence = []
    for word, start, end in word_list:
        current_sentence.append((word, start, end))
        if word.endswith(('.', '!', '?')):
            sentence_text = ' '.join([w for w, _, _ in current_sentence])
            sentence_start = current_sentence[0][1]
            sentence_end = current_sentence[-1][2]
            sentences.append({
                "start": sentence_start,
                "end": sentence_end,
                "text": sentence_text
            })
            current_sentence = []
    
    if current_sentence:
        sentence_text = ' '.join([w for w, _, _ in current_sentence])
        sentence_start = current_sentence[0][1]
        sentence_end = current_sentence[-1][2]
        sentences.append({
            "start": sentence_start,
            "end": sentence_end,
            "text": sentence_text
        })
    
    return sentences

def transcribe_video(vid_path):
    if not vid_path.endswith('.mp4'):
        raise ValueError("Only mp4 videos are supported")
    
    audio_path = vid_path.replace('.mp4', '.wav')
    output_path = vid_path.replace('.mp4', '_transcription.txt')
    
    extract_AUDIO(vid_path, audio_path)
    run_whisper_cpp(audio_path, output_path)
    
    segments = parse_whisper_output(output_path)
    transcription = ' '.join([seg['text'] for seg in segments])
    
    return transcription, segments
