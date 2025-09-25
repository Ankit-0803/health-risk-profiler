# Input validation
from config import Config
import os

def validate_input(data):
    """Validate text input data"""
    if not isinstance(data, dict):
        return {"valid": False, "reason": "Input must be a dictionary"}
    
    required_fields = Config.REQUIRED_FIELDS
    missing_required = [field for field in required_fields if field not in data]
    
    if len(missing_required) / len(required_fields) > 0.5:
        return {
            "valid": False, 
            "reason": f">50% required fields missing: {missing_required}"
        }
    
    return {"valid": True, "reason": "Input is valid"}

def validate_image(file):
    """Validate uploaded image file"""
    if not file:
        return False
    
    # Check file extension
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    filename = file.filename.lower()
    
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1]
    if extension not in allowed_extensions:
        return False
    
    # Check file size (optional - Flask config handles this)
    return True
