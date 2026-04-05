"""
Configuration file for TextPal application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask Configuration
class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'textpal-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', True)
    
    # Upload configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 52428800))  # 50MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    
    # CORS configuration
    CORS_ENABLED = os.getenv('CORS_ENABLED', True)
    
    # Model configuration
    DOWNLOAD_MODELS = os.getenv('DOWNLOAD_MODELS', True)
    
    # Text processing defaults
    SUMMARIZATION_MAX_LENGTH = int(os.getenv('SUMMARIZATION_MAX_LENGTH', 150))
    SUMMARIZATION_MIN_LENGTH = int(os.getenv('SUMMARIZATION_MIN_LENGTH', 50))
    KEYWORDS_COUNT = int(os.getenv('KEYWORDS_COUNT', 10))
    QA_CONTEXT_LIMIT = int(os.getenv('QA_CONTEXT_LIMIT', 3000))


class DevelopmentConfig(Config):
    """Development configuration"""
    TESTING = False
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    TESTING = False
    DEBUG = False
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://yourdomain.com').split(',')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration object based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
