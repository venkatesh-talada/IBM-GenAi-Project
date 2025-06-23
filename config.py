import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API Keys  
    GRANITE_API_KEY = os.environ.get('GRANITE_API_KEY')
    HUGGINGFACE_API_TOKEN = os.environ.get('HUGGINGFACE_API_TOKEN')
    
    # Model Configuration
    MODEL_NAME = os.environ.get('MODEL_NAME', 'ibm-granite/granite-3.3-2b-instruct')
    MAX_LENGTH = int(os.environ.get('MAX_LENGTH', 2048))
    TEMPERATURE = float(os.environ.get('TEMPERATURE', 0.7))
    
    # Database Configuration (for future use)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Redis Configuration (for future use)
    REDIS_URL = os.environ.get('REDIS_URL')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # Ensure secret key is set in production
    @classmethod
    def init_app(cls, app):
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set in production")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 