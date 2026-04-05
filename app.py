"""
Smart Reading Assistant (TextPal) - Flask Backend
Main application file
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# Import utility modules
from utils.text_extraction import extract_text
from utils.text_processing import (
    calculate_flesch_reading_ease,
    summarize_text,
    extract_keywords
)
from utils.translation import translate_to_tamil, translate_to_english, detect_language
from utils.chatbot import SimpleChatbot


# Flask app configuration
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize chatbot
chatbot = SimpleChatbot()
current_text = ""


def allowed_file(filename):
    """
    Check if file extension is allowed
    
    Args:
        filename (str): Name of the file
        
    Returns:
        bool: True if allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and text extraction
    
    Returns:
        JSON: Extracted text and file info
    """
    global current_text, chatbot
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only .txt and .pdf files are allowed'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text
        extracted_text = extract_text(filepath)
        
        if extracted_text.startswith('Error') or extracted_text.startswith('Unsupported'):
            return jsonify({'error': extracted_text}), 400
        
        # Store for later use
        current_text = extracted_text
        chatbot.set_context(extracted_text)
        
        # Return success response
        return jsonify({
            'success': True,
            'filename': file.filename,
            'text': extracted_text,
            'char_count': len(extracted_text),
            'word_count': len(extracted_text.split())
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@app.route('/api/analyze-difficulty', methods=['POST'])
def analyze_difficulty():
    """
    Analyze reading difficulty of text
    
    Returns:
        JSON: Difficulty analysis results
    """
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        analysis = calculate_flesch_reading_ease(text)
        return jsonify(analysis), 200
    except Exception as e:
        return jsonify({'error': f'Error analyzing text: {str(e)}'}), 500


@app.route('/api/summarize', methods=['POST'])
def summarize():
    """
    Generate text summary
    
    Returns:
        JSON: Summarized text
    """
    data = request.get_json()
    text = data.get('text', '')
    max_length = data.get('max_length', 150)
    min_length = data.get('min_length', 50)
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        summary = summarize_text(text, max_length=max_length, min_length=min_length)
        return jsonify({
            'summary': summary,
            'original_length': len(text),
            'summary_length': len(summary)
        }), 200
    except Exception as e:
        return jsonify({'error': f'Error summarizing text: {str(e)}'}), 500


@app.route('/api/extract-keywords', methods=['POST'])
def get_keywords():
    """
    Extract keywords from text
    
    Returns:
        JSON: List of keywords
    """
    data = request.get_json()
    text = data.get('text', '')
    num_keywords = data.get('num_keywords', 10)
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        keywords = extract_keywords(text, num_keywords=num_keywords)
        return jsonify({'keywords': keywords}), 200
    except Exception as e:
        return jsonify({'error': f'Error extracting keywords: {str(e)}'}), 500


@app.route('/api/translate', methods=['POST'])
def translate():
    """
    Translate text between English and Tamil
    
    Returns:
        JSON: Translated text
    """
    data = request.get_json()
    text = data.get('text', '')
    target_language = data.get('target_language', 'ta')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        if target_language == 'ta':
            translated = translate_to_tamil(text)
        elif target_language == 'en':
            translated = translate_to_english(text)
        else:
            return jsonify({'error': 'Unsupported language'}), 400
        
        return jsonify({
            'original_text': text,
            'translated_text': translated,
            'target_language': target_language
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error translating text: {str(e)}'}), 500


@app.route('/api/detect-language', methods=['POST'])
def detect_lang():
    """
    Detect language of text
    
    Returns:
        JSON: Detected language
    """
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        from utils.translation import detect_language
        language = detect_language(text)
        lang_name = 'Tamil' if language == 'ta' else 'English'
        return jsonify({'language': language, 'language_name': lang_name}), 200
    except Exception as e:
        return jsonify({'error': f'Error detecting language: {str(e)}'}), 500


@app.route('/api/ask-question', methods=['POST'])
def ask_question():
    """
    Ask chatbot a question about the current text
    
    Returns:
        JSON: Answer to the question
    """
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    if not current_text:
        return jsonify({'error': 'No document loaded. Please upload a file first.'}), 400
    
    try:
        answer = chatbot.ask_question(question)
        return jsonify({
            'question': question,
            'answer': answer,
            'conversation_history': chatbot.get_conversation_history()
        }), 200
    except Exception as e:
        return jsonify({'error': f'Error processing question: {str(e)}'}), 500


@app.route('/api/chat-history', methods=['GET'])
def get_chat_history():
    """
    Get conversation history
    
    Returns:
        JSON: Conversation history
    """
    try:
        history = chatbot.get_conversation_history()
        return jsonify({'history': history}), 200
    except Exception as e:
        return jsonify({'error': f'Error retrieving history: {str(e)}'}), 500


@app.route('/api/clear-chat', methods=['POST'])
def clear_chat():
    """Clear conversation history"""
    try:
        chatbot.clear_history()
        return jsonify({'success': True, 'message': 'Chat history cleared'}), 200
    except Exception as e:
        return jsonify({'error': f'Error clearing chat: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'TextPal API is running'}), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
