import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Health survey fields
    REQUIRED_FIELDS = ['age', 'smoker', 'exercise', 'diet']
    OPTIONAL_FIELDS = ['alcohol', 'sleep', 'stress', 'family_history']
    
    # Risk scoring weights
    RISK_WEIGHTS = {
        'smoking': 25,
        'poor_diet': 20,
        'low_exercise': 15,
        'excessive_alcohol': 15,
        'poor_sleep': 10,
        'high_stress': 10,
        'family_history': 15
    }
    
    # Minimum confidence threshold
    MIN_CONFIDENCE = 0.7
