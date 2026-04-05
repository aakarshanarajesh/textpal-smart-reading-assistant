"""
Test suite for TextPal application
Run with: pytest
"""

import pytest
import json
import os
from app import app
from utils.text_processing import (
    calculate_flesch_reading_ease,
    summarize_text,
    extract_keywords,
    count_syllables
)
from utils.translation import detect_language
from utils.text_extraction import extract_text


@pytest.fixture
def client():
    """Create Flask test client"""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    
    os.makedirs('test_uploads', exist_ok=True)
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    import shutil
    if os.path.exists('test_uploads'):
        shutil.rmtree('test_uploads')


class TestTextProcessing:
    """Test text processing utilities"""
    
    def test_flesch_reading_ease(self):
        """Test Flesch Reading Ease calculation"""
        text = "The quick brown fox jumps over the lazy dog. " * 10
        result = calculate_flesch_reading_ease(text)
        
        assert 'score' in result
        assert 'level' in result
        assert 0 <= result['score'] <= 100
    
    def test_syllable_counting(self):
        """Test syllable counter"""
        count = count_syllables("hello world")
        assert count > 0
    
    def test_keyword_extraction(self):
        """Test keyword extraction"""
        text = "Machine learning is a subset of artificial intelligence. AI is transforming technology."
        keywords = extract_keywords(text, num_keywords=5)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 5


class TestLanguageDetection:
    """Test language detection"""
    
    def test_english_detection(self):
        """Test English text detection"""
        text = "This is an English sentence."
        lang = detect_language(text)
        assert lang == 'en'
    
    def test_tamil_detection(self):
        """Test Tamil text detection"""
        text = "இது தமிழ் உரை"
        lang = detect_language(text)
        assert lang == 'ta'


class TestAPIEndpoints:
    """Test Flask API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_analyze_difficulty_endpoint(self, client):
        """Test difficulty analysis endpoint"""
        text = "The quick brown fox jumps over the lazy dog. " * 20
        response = client.post(
            '/api/analyze-difficulty',
            json={'text': text},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'score' in data
        assert 'level' in data
    
    def test_analyze_difficulty_empty_text(self, client):
        """Test difficulty analysis with empty text"""
        response = client.post(
            '/api/analyze-difficulty',
            json={'text': ''},
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_extract_keywords_endpoint(self, client):
        """Test keyword extraction endpoint"""
        text = "Python is a programming language. Java is also a programming language."
        response = client.post(
            '/api/extract-keywords',
            json={'text': text, 'num_keywords': 5},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'keywords' in data
        assert isinstance(data['keywords'], list)
    
    def test_detect_language_endpoint(self, client):
        """Test language detection endpoint"""
        response = client.post(
            '/api/detect-language',
            json={'text': 'Hello world'},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'language' in data
    
    def test_ask_question_no_document(self, client):
        """Test asking question without loaded document"""
        response = client.post(
            '/api/ask-question',
            json={'question': 'What is this about?'},
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_invalid_endpoint(self, client):
        """Test invalid endpoint"""
        response = client.get('/api/invalid-endpoint')
        assert response.status_code == 404


class TestFileHandling:
    """Test file handling"""
    
    def test_txt_extraction(self, tmp_path):
        """Test TXT file extraction"""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("This is a test document.")
        
        # Extract text
        text = extract_text(str(test_file))
        assert "test document" in text
    
    def test_unsupported_format(self, tmp_path):
        """Test unsupported file format"""
        # Create test file with unsupported format
        test_file = tmp_path / "test.docx"
        test_file.write_text("Dummy content")
        
        # Try to extract
        text = extract_text(str(test_file))
        assert "Unsupported" in text or "Error" in text


class TestChatbot:
    """Test chatbot functionality"""
    
    def test_chatbot_initialization(self):
        """Test chatbot initialization"""
        from utils.chatbot import SimpleChatbot
        bot = SimpleChatbot()
        assert bot.context == ""
        assert bot.conversation_history == []
    
    def test_chatbot_set_context(self):
        """Test setting chatbot context"""
        from utils.chatbot import SimpleChatbot
        bot = SimpleChatbot()
        text = "This is test context for the chatbot."
        bot.set_context(text)
        assert bot.context == text
    
    def test_chat_history(self):
        """Test conversation history"""
        from utils.chatbot import SimpleChatbot
        bot = SimpleChatbot()
        bot.set_context("Sample text for testing.")
        
        history = bot.get_conversation_history()
        assert isinstance(history, list)


def test_app_creation():
    """Test Flask app is created properly"""
    assert app is not None
    assert app.config['TESTING'] == False


def test_app_routes():
    """Test that required routes exist"""
    routes = [route.rule for route in app.url_map.iter_rules()]
    
    # Check essential routes
    assert '/' in routes
    assert '/api/upload' in routes
    assert '/api/analyze-difficulty' in routes
    assert '/api/summarize' in routes
    assert '/api/extract-keywords' in routes


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
