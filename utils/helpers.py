# Helper functions
import os
import logging

def cleanup_uploads(filepath):
    """Clean up uploaded files"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        logging.warning(f"Failed to cleanup file {filepath}: {str(e)}")

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
