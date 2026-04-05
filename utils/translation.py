"""
Translation Module
Handles translation between Tamil and English
"""

from transformers import pipeline
import requests


# Initialize translation pipeline
try:
    en_to_tamil = pipeline("translation_en_to_ta", model="Helsinki-NLP/opus-mt-en-ta", device=-1)
    tamil_to_en = pipeline("translation_ta_to_en", model="Helsinki-NLP/opus-mt-ta-en", device=-1)
except:
    en_to_tamil = None
    tamil_to_en = None


def translate_to_tamil(text):
    """
    Translate English text to Tamil
    
    Args:
        text (str): English text to translate
        
    Returns:
        str: Tamil translation
    """
    if not en_to_tamil:
        return "Translation service unavailable. Please install required models."
    
    try:
        # Split text into chunks if too long (model has token limits)
        if len(text.split()) > 512:
            chunks = [' '.join(text.split()[i:i+512]) for i in range(0, len(text.split()), 512)]
            translations = [en_to_tamil(chunk)[0]['translation_text'] for chunk in chunks]
            return ' '.join(translations)
        
        result = en_to_tamil(text)
        return result[0]['translation_text']
    except Exception as e:
        return f"Translation error: {str(e)}"


def translate_to_english(text):
    """
    Translate Tamil text to English
    
    Args:
        text (str): Tamil text to translate
        
    Returns:
        str: English translation
    """
    if not tamil_to_en:
        return "Translation service unavailable. Please install required models."
    
    try:
        # Split text into chunks if too long
        if len(text.split()) > 512:
            chunks = [' '.join(text.split()[i:i+512]) for i in range(0, len(text.split()), 512)]
            translations = [tamil_to_en(chunk)[0]['translation_text'] for chunk in chunks]
            return ' '.join(translations)
        
        result = tamil_to_en(text)
        return result[0]['translation_text']
    except Exception as e:
        return f"Translation error: {str(e)}"


def detect_language(text):
    """
    Simple language detection based on characters
    
    Args:
        text (str): Text to detect language for
        
    Returns:
        str: Either 'en' for English or 'ta' for Tamil
    """
    tamil_chars = set('அஆஇஈஉஊ஋஌எஏஐஒஓஔஃ')
    
    for char in text:
        if char in tamil_chars:
            return 'ta'
    
    return 'en'
