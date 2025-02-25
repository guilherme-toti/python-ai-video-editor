import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("pt_core_news_sm")

def analyze_text(transcription, segments):
    """
    Analyze transcription to identify segments to keep (removing breaths, mistakes, repeats).
    
    Args:
        transcription (str): Full transcription text.
        segments (list): List of segments with timestamps and text.
    
    Returns:
        list: Segments to keep (with start, end times and text).
    """
    # Tokenize and process text
    doc = nlp(transcription)
    sentences = [sent.text for sent in doc.sents]
    
    # Identify filler words and hesitations
    filler_words = {"hum", "é", "tipo", "então", "ah", "bem"}
    mistake_indices = []
    for token in doc:
        if token.text.lower() in filler_words or token.is_stop:
            mistake_indices.append(token.sent.start)
    
    # Detect repeated sentences
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    repeats = []
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            if similarity_matrix[i][j] > 0.8:  # Threshold for similarity
                repeats.append((i, j))
    
    # Keep last repeat, remove earlier ones
    to_remove = set()
    for i, j in repeats:
        to_remove.add(i)  # Remove earlier sentence
    
    # Also remove mistakes
    to_remove.update(mistake_indices)
    
    # Map segments to sentences and filter
    segments_to_keep = []
    for segment in segments:
        segment_text = segment["text"]
        segment_doc = nlp(segment_text)
        segment_sents = [sent.text for sent in segment_doc.sents]
        
        # Check if any sentence in segment should be removed
        should_remove = False
        for sent in segment_sents:
            sent_idx = sentences.index(sent) if sent in sentences else -1
            if sent_idx in to_remove:
                should_remove = True
                break
        
        if not should_remove:
            segments_to_keep.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment_text
            })
    
    return segments_to_keep
