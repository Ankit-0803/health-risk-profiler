# OCR and text parsing
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
import json
from config import Config
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRProcessor:
    def __init__(self):
        self.required_fields = Config.REQUIRED_FIELDS
        self.optional_fields = Config.OPTIONAL_FIELDS
        self.all_fields = self.required_fields + self.optional_fields
    
    def parse_text(self, data):
        """Parse text input and extract health survey data"""
        try:
            answers = {}
            missing_fields = []
            
            # Process each field
            for field in self.all_fields:
                if field in data:
                    answers[field] = self._normalize_field_value(field, data[field])
                elif field in self.required_fields:
                    missing_fields.append(field)
            
            # Calculate confidence based on completeness
            total_fields = len(self.required_fields)
            completed_fields = total_fields - len(missing_fields)
            confidence = completed_fields / total_fields
            
            # Check if profile is incomplete
            if len(missing_fields) / len(self.required_fields) > 0.5:
                return {
                    "status": "incomplete_profile",
                    "reason": f">50% fields missing: {missing_fields}"
                }
            
            return {
                "answers": answers,
                "missing_fields": missing_fields,
                "confidence": round(confidence, 2)
            }
            
        except Exception as e:
            return {"error": f"Text parsing error: {str(e)}"}
    
    def parse_image(self, image_path):
        """Parse image using OCR and extract health survey data"""
        try:
            # Preprocess image
            processed_image = self._preprocess_image(image_path)
            
            # Extract text using OCR
            extracted_text = pytesseract.image_to_string(processed_image)
            
            # Parse extracted text
            parsed_data = self._parse_extracted_text(extracted_text)
            
            return self.parse_text(parsed_data)
            
        except Exception as e:
            return {"error": f"OCR processing error: {str(e)}"}
    
    def _preprocess_image(self, image_path):
        """Preprocess image for better OCR results"""
        # Read image
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply noise reduction
        denoised = cv2.medianBlur(gray, 5)
        
        # Apply threshold to get image with only black and white
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def _parse_extracted_text(self, text):
        """Parse OCR extracted text to find health survey fields"""
        parsed_data = {}
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip().lower()
            if not line:
                continue
            
            # Age parsing
            if 'age' in line:
                age_match = re.search(r'age[:\s]*(\d+)', line)
                if age_match:
                    parsed_data['age'] = int(age_match.group(1))
            
            # Smoker parsing
            elif 'smok' in line:
                if any(word in line for word in ['yes', 'true', 'y']):
                    parsed_data['smoker'] = True
                elif any(word in line for word in ['no', 'false', 'n']):
                    parsed_data['smoker'] = False
            
            # Exercise parsing
            elif 'exercise' in line or 'activity' in line:
                if 'rarely' in line or 'never' in line:
                    parsed_data['exercise'] = 'rarely'
                elif 'sometimes' in line or 'moderate' in line:
                    parsed_data['exercise'] = 'sometimes'
                elif 'often' in line or 'regular' in line:
                    parsed_data['exercise'] = 'often'
                elif 'daily' in line:
                    parsed_data['exercise'] = 'daily'
            
            # Diet parsing
            elif 'diet' in line or 'food' in line:
                if 'high sugar' in line or 'sweet' in line:
                    parsed_data['diet'] = 'high sugar'
                elif 'balanced' in line:
                    parsed_data['diet'] = 'balanced'
                elif 'low fat' in line:
                    parsed_data['diet'] = 'low fat'
                elif 'vegetarian' in line:
                    parsed_data['diet'] = 'vegetarian'
            
            # Alcohol parsing
            elif 'alcohol' in line or 'drink' in line:
                if 'never' in line or 'no' in line:
                    parsed_data['alcohol'] = 'never'
                elif 'rarely' in line:
                    parsed_data['alcohol'] = 'rarely'
                elif 'moderate' in line:
                    parsed_data['alcohol'] = 'moderate'
                elif 'heavy' in line or 'excessive' in line:
                    parsed_data['alcohol'] = 'heavy'
        
        return parsed_data
    
    def _normalize_field_value(self, field, value):
        """Normalize field values to standard format"""
        if field == 'age':
            return int(value) if isinstance(value, (int, str)) else value
        
        elif field == 'smoker':
            if isinstance(value, str):
                return value.lower() in ['yes', 'true', 'y', '1']
            return bool(value)
        
        elif field in ['exercise', 'diet', 'alcohol', 'sleep', 'stress']:
            return str(value).lower().strip()
        
        return value
