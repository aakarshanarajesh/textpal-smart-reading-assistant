"""
TextPal Utils Package
Contains utility modules for text processing, extraction, and translation
"""

from .text_extraction import extract_text
from .text_processing import (
    calculate_flesch_reading_ease,
    summarize_text,
    extract_keywords,
    simple_extractive_summary,
    count_syllables
)
from .translation import translate_to_tamil, translate_to_english, detect_language
from .chatbot import SimpleChatbot

__all__ = [
    'extract_text',
    'calculate_flesch_reading_ease',
    'summarize_text',
    'extract_keywords',
    'translate_to_tamil',
    'translate_to_english',
    'detect_language',
    'SimpleChatbot'
]
