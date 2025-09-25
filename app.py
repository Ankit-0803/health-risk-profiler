from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from PIL import Image

from config import Config
from models.ocr_processor import OCRProcessor
from models.factor_extractor import FactorExtractor
from models.risk_classifier import RiskClassifier
from models.recommender import Recommender
from utils.validators import validate_input, validate_image
from utils.helpers import cleanup_uploads

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize processors
ocr_processor = OCRProcessor()
factor_extractor = FactorExtractor()
risk_classifier = RiskClassifier()
recommender = Recommender()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "AI-Powered Health Risk Profiler",
        "version": "1.0.0",
        "endpoints": [
            "/parse-text",
            "/parse-image", 
            "/extract-factors",
            "/classify-risk",
            "/get-recommendations",
            "/analyze-complete"
        ]
    })

@app.route('/parse-text', methods=['POST'])
def parse_text():
    """Step 1: Parse text input and extract health survey data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate input
        validation_result = validate_input(data)
        if not validation_result['valid']:
            return jsonify({
                "status": "incomplete_profile",
                "reason": validation_result['reason']
            }), 400
        
        # Process text input
        result = ocr_processor.parse_text(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/parse-image', methods=['POST'])
def parse_image():
    """Step 1: Parse image input using OCR"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Validate image
        if not validate_image(file):
            return jsonify({"error": "Invalid image format"}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process image
            result = ocr_processor.parse_image(filepath)
            
            # Cleanup uploaded file
            cleanup_uploads(filepath)
            
            return jsonify(result)
            
        except Exception as e:
            cleanup_uploads(filepath)
            raise e
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/extract-factors', methods=['POST'])
def extract_factors():
    """Step 2: Extract risk factors from parsed answers"""
    try:
        data = request.get_json()
        
        if not data or 'answers' not in data:
            return jsonify({"error": "No answers data provided"}), 400
        
        result = factor_extractor.extract_factors(data['answers'])
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/classify-risk', methods=['POST'])
def classify_risk():
    """Step 3: Classify risk level based on factors"""
    try:
        data = request.get_json()
        
        if not data or 'factors' not in data:
            return jsonify({"error": "No factors data provided"}), 400
        
        result = risk_classifier.classify_risk(data['factors'])
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    """Step 4: Generate recommendations based on risk profile"""
    try:
        data = request.get_json()
        
        required_fields = ['risk_level', 'factors']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields: risk_level, factors"}), 400
        
        result = recommender.generate_recommendations(
            data['risk_level'], 
            data['factors']
        )
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze-complete', methods=['POST'])
def analyze_complete():
    """Complete pipeline: Process input through all 4 steps"""
    try:
        # Handle both text and image inputs
        if request.content_type.startswith('multipart/form-data'):
            # Image input
            if 'image' not in request.files:
                return jsonify({"error": "No image file provided"}), 400
            
            file = request.files['image']
            if not validate_image(file):
                return jsonify({"error": "Invalid image format"}), 400
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Step 1: Parse image
                parse_result = ocr_processor.parse_image(filepath)
                cleanup_uploads(filepath)
                
            except Exception as e:
                cleanup_uploads(filepath)
                raise e
                
        else:
            # Text input
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            validation_result = validate_input(data)
            if not validation_result['valid']:
                return jsonify({
                    "status": "incomplete_profile",
                    "reason": validation_result['reason']
                }), 400
            
            # Step 1: Parse text
            parse_result = ocr_processor.parse_text(data)
        
        # Check if parsing was successful
        if 'status' in parse_result and parse_result['status'] == 'incomplete_profile':
            return jsonify(parse_result), 400
        
        # Step 2: Extract factors
        factor_result = factor_extractor.extract_factors(parse_result['answers'])
        
        # Step 3: Classify risk
        risk_result = risk_classifier.classify_risk(factor_result['factors'])
        
        # Step 4: Generate recommendations
        recommendation_result = recommender.generate_recommendations(
            risk_result['risk_level'], 
            factor_result['factors']
        )
        
        # Combine all results
        complete_result = {
            "parsing": parse_result,
            "factors": factor_result,
            "risk_classification": risk_result,
            "recommendations": recommendation_result,
            "status": "ok"
        }
        
        return jsonify(complete_result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Starting Flask app on http://127.0.0.1:8080")
    app.run(debug=True, host='127.0.0.1', port=8080, threaded=True)

