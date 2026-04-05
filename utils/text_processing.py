"""
Text Processing Module
Handles text summarization, difficulty analysis, and keyword extraction
"""

import re
from collections import Counter
from transformers import pipeline


# Initialize summarization pipeline (using BART model)
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
except:
    summarizer = None


def calculate_flesch_reading_ease(text):
    """
    Calculate Flesch Reading Ease score
    Higher score = easier to read (0-100 scale)
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        dict: Dictionary with score and difficulty level
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Count sentences (approximate)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    num_sentences = len(sentences)
    
    # Count words
    words = text.split()
    num_words = len(words)
    
    # Count syllables (approximation)
    num_syllables = count_syllables(text)
    
    # Avoid division by zero
    if num_words == 0 or num_sentences == 0:
        return {"score": 0, "level": "Unknown", "description": "Insufficient text"}
    
    # Flesch Reading Ease formula
    # Score = 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
    score = 206.835 - (1.015 * (num_words / num_sentences)) - (84.6 * (num_syllables / num_words))
    score = max(0, min(100, score))  # Clamp between 0 and 100
    
    # Determine difficulty level
    if score >= 90:
        level = "Very Easy"
    elif score >= 80:
        level = "Easy"
    elif score >= 70:
        level = "Fairly Easy"
    elif score >= 60:
        level = "Standard"
    elif score >= 50:
        level = "Fairly Difficult"
    elif score >= 30:
        level = "Difficult"
    else:
        level = "Very Difficult"
    
    return {
        "score": round(score, 2),
        "level": level,
        "num_words": num_words,
        "num_sentences": num_sentences
    }


def count_syllables(text):
    """
    Approximate syllable counting
    
    Args:
        text (str): Text to count syllables in
        
    Returns:
        int: Approximate number of syllables
    """
    words = text.lower().split()
    syllable_count = 0
    vowels = "aeiouy"
    previous_was_vowel = False
    
    for word in words:
        word = re.sub(r"[^a-z]", "", word)
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent e
        if word.endswith("e"):
            syllable_count -= 1
        
        # Ensure at least 1 syllable per word
        if syllable_count == 0 and word:
            syllable_count = 1
    
    return syllable_count


def summarize_text(text, max_length=150, min_length=50):
    """
    Summarize text using transformer model
    
    Args:
        text (str): Input text to summarize
        max_length (int): Maximum length of summary
        min_length (int): Minimum length of summary
        
    Returns:
        str: Summarized text
    """
    if not summarizer:
        # Fallback to simple extractive summarization if model not available
        return simple_extractive_summary(text)
    
    try:
        # If text is too long, truncate it for the model
        if len(text.split()) > 1024:
            text = ' '.join(text.split()[:1024])
        
        # Use transformer summarizer
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except:
        # Fallback to simple summarization
        return simple_extractive_summary(text)


def simple_extractive_summary(text, num_sentences=3):
    """
    Simple extractive summarization using sentence scoring
    
    Args:
        text (str): Input text to summarize
        num_sentences (int): Number of sentences to include in summary
        
    Returns:
        str: Summary of the text
    """
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= num_sentences:
        return text[:500]  # Return truncated if not enough sentences
    
    # Score sentences based on word frequency
    words = text.lower().split()
    word_freq = Counter(words)
    
    # Remove common words
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'was', 'are', 'were'}
    word_freq = {word: freq for word, freq in word_freq.items() if word not in common_words}
    
    # Score sentences
    sentence_scores = {}
    for idx, sentence in enumerate(sentences):
        for word in sentence.lower().split():
            if word in word_freq:
                sentence_scores[idx] = sentence_scores.get(idx, 0) + word_freq[word]
    
    # Get top sentences in original order
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    top_sentences = sorted(top_sentences)  # Sort by original order
    
    summary = '. '.join([sentences[i] for i in top_sentences]) + '.'
    return summary[:500]  # Limit to 500 characters


def extract_keywords(text, num_keywords=10):
    """
    Extract important keywords from text
    
    Args:
        text (str): Input text
        num_keywords (int): Number of keywords to extract
        
    Returns:
        list: List of important keywords
    """
    # Remove URLs and special characters
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Split into words
    words = text.split()
    
    # Remove common words
    common_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
        'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
        'can', 'with', 'without', 'from', 'by', 'as', 'if', 'while', 'which', 'who'
    }
    
    filtered_words = [word for word in words if word not in common_words and len(word) > 2]
    
    # Count word frequency
    word_freq = Counter(filtered_words)
    
    # Get top keywords
    keywords = [word for word, _ in word_freq.most_common(num_keywords)]
    
    return keywords
