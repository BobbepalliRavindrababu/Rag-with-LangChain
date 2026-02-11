"""
Production Configuration Module
Use this for production deployment with environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/tenants.db')
    
    # Email
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '')
    
    # Application
    APP_NAME = os.getenv('APP_NAME', 'Tenant Management System')
    PG_NAME = os.getenv('PG_NAME', 'My PG')
    
    # QR Codes
    QR_CODE_DIR = os.getenv('QR_CODE_DIR', 'static/qrcodes')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
    
    # Security
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Features
    ENABLE_EMAIL = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'True').lower() == 'true'
    ENABLE_QR = os.getenv('ENABLE_QR_GENERATION', 'True').lower() == 'true'
    
    # Limits
    MAX_TENANTS = int(os.getenv('MAX_TENANTS', 1000))
    MAX_UPLOAD_SIZE_MB = int(os.getenv('MAX_UPLOAD_SIZE_MB', 10))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    HOST = 'localhost'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_PATH = ':memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}


def get_config(config_name='default'):
    """Get configuration by name"""
    return config.get(config_name, config['default'])


# Usage Example:
if __name__ == '__main__':
    # Print current configuration
    cfg = Config()
    print("Current Configuration:")
    print(f"  SECRET_KEY: {'*' * 20} (hidden)")
    print(f"  DEBUG: {cfg.DEBUG}")
    print(f"  HOST: {cfg.HOST}")
    print(f"  PORT: {cfg.PORT}")
    print(f"  DATABASE: {cfg.DATABASE_PATH}")
    print(f"  EMAIL: {'Configured' if cfg.SENDER_EMAIL else 'Not configured (test mode)'}")
    print(f"  QR CODES: {cfg.QR_CODE_DIR}")
    print(f"  BASE URL: {cfg.BASE_URL}")
