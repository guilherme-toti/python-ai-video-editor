import ollama

def generate_captions(segments_to_keep):
    """
    Generate captions from the segments to keep.
    
    Args:
        segments_to_keep (list): List of segments with text.
    
    Returns:
        str: Captions text.
    """
    captions = " ".join([seg["text"] for seg in segments_to_keep])
    return captions

def generate_social_media_content(transcription):
    """
    Generate LinkedIn and Threads content based on transcription.
    
    Args:
        transcription (str): Full transcription text.
    
    Returns:
        tuple: (LinkedIn content, Threads content).
    """
    prompt_linkedin = (
        f"Generate a professional LinkedIn post based on this video transcript "
        f"(in Brazilian Portuguese): {transcription}"
    )
    linkedin_content = ollama.generate(model="llama2", prompt=prompt_linkedin)["response"]
    
    prompt_threads = (
        f"Generate an informal Threads post based on this video transcript "
        f"(in Brazilian Portuguese): {transcription}"
    )
    threads_content = ollama.generate(model="llama2", prompt=prompt_threads)["response"]
    
    return linkedin_content, threads_content
