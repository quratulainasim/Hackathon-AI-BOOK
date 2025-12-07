"""
Logging Configuration for AI-BOOK RAG Chatbot Backend
"""

import logging
import sys
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Set up logging configuration for the application"""

    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def get_logger(name: str):
    """Get a logger with the specified name"""
    return logging.getLogger(name)

# Initialize logging when module is imported
setup_logging()

# Example usage:
# logger = get_logger(__name__)
# logger.info("Application started")