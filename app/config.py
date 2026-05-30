import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-change-this'
    JSON_SORT_KEYS = False
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # App settings
    APP_NAME = 'Library Management System'

    # Default suppliers shown when adding a new book
    DEFAULT_NHA_CUNG_CAPS = [
        {'ma_ncc': 'NCC01', 'ten_ncc': 'Fahasa'},
        {'ma_ncc': 'NCC02', 'ten_ncc': 'Tiki Trading'},
        {'ma_ncc': 'NCC03', 'ten_ncc': 'Nhã Nam'},
        {'ma_ncc': 'NCC04', 'ten_ncc': 'NXB Trẻ'},
        {'ma_ncc': 'NCC05', 'ten_ncc': 'First News'},
        {'ma_ncc': 'NCC06', 'ten_ncc': 'NXB Chính trị'},
        {'ma_ncc': 'NCC07', 'ten_ncc': 'Nhà sách Phương Nam'},
        {'ma_ncc': 'NCC08', 'ten_ncc': 'Alpha Books'},
        {'ma_ncc': 'NCC09', 'ten_ncc': 'Nhà sách Kim Đồng'},
    ]
    
    # Fine settings
    FINE_PER_DAY = 5000  # VND per day
    BORROW_DAYS = 30

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
