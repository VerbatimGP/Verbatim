import re
from collections import defaultdict
from heapq import nlargest

def generate_summary(text, num_sentences=3):
    def clean_text(text):
        text = re.sub(r'[^\w\s.]', '', text)
        return text.strip()

    def get_sentences(text):
        return [s.strip() for s in text.split('.') if s.strip()]

    def calculate_word_freq(text):
        words = text.lower().split()
        freq = defaultdict(int)
        for word in words:
            freq[word] += 1
        return freq

    def score_sentences(sentences, word_freq):
        scores = defaultdict(int)
        for i, sentence in enumerate(sentences):
            for word in sentence.lower().split():
                scores[i] += word_freq[word]
            scores[i] = scores[i] // max(len(sentence.split()), 1)
        return scores

    if not text or len(text.split()) < 20:
        return "Text too short for summarization"
    
    cleaned_text = clean_text(text)
    sentences = get_sentences(cleaned_text)
    
    if len(sentences) <= num_sentences:
        return text
    
    word_freq = calculate_word_freq(cleaned_text)
    sentence_scores = score_sentences(sentences, word_freq)
    
    summary_indexes = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary_indexes.sort()
    
    summary = '. '.join(sentences[i] for i in summary_indexes) + '.'
    
    return summary
