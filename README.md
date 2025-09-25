# AI-Powered Health Risk Profiler Backend

## **Overview**

This project provides a Flask‐based API backend that processes health survey data via **text** or **scanned images**. It uses **OCR** for image parsing, extracts critical health risk factors, classifies risk levels, and generates personalized recommendations. This backend is exposed publicly via an **ngrok** tunnel for easy remote testing and demo.

---

## **Live Demo URL (ngrok)**

[**https://saul-repoussa-articulately.ngrok-free.dev**](https://saul-repoussa-articulately.ngrok-free.dev)

_All API requests should be sent to the above base URL._

---

## **Features**

- Supports survey input as **JSON (text)** or **uploaded image (OCR)**  
- Accurate extraction and normalization of health factors  
- **Risk classification** with **confidence scoring** and **rationale**  
- Tailored **non-diagnostic** recommendations  
- Robust **guardrails** for incomplete or invalid inputs  
- Clear **JSON** responses with meaningful error messages  

---

## **Setup Instructions**

### **Prerequisites**

- **Python 3.8+**  
- **Tesseract OCR** installed and in your system `PATH`  
  _Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)_  
- **ngrok** for public tunneling  

### **Installation**

1. Clone repo
git clone https://github.com/yourusername/health-risk-profiler.git
cd health-risk-profiler

2. Create virtual environment
python -m venv venv

3. Activate venv
Windows
venv\Scripts\activate

Linux/Mac
source venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

text

### **Run the Backend Locally**

python app.py

text

### **Expose via ngrok**

In a new terminal:

ngrok http 8080

text

_Use the displayed HTTPS URL above as the base for API calls._

---

## **API Endpoints**

| **Endpoint**           | **Method** | **Description**                            |
|------------------------|------------|--------------------------------------------|
| `/`                    | GET        | Health check, service status               |
| `/parse-text`          | POST       | Parse survey data JSON                     |
| `/parse-image`         | POST       | Parse uploaded survey image (OCR)          |
| `/extract-factors`     | POST       | Extract risk factors from survey answers   |
| `/classify-risk`       | POST       | Classify risk based on factors             |
| `/get-recommendations` | POST       | Generate recommendations                   |
| `/analyze-complete`    | POST       | Complete pipeline: parse → classify → recommend |

---

## **Sample CURL Requests**

_Replace the base URL if your ngrok URL changes._

Health Check
curl -X GET https://saul-repoussa-articulately.ngrok-free.dev/

Parse Text
curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/parse-text
-H "Content-Type: application/json"
-d '{"age":42,"smoker":true,"exercise":"rarely","diet":"high sugar"}'

Parse Image (adjust path to your image file)
curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/parse-image
-F "image=@survey-form.jpg"

Extract Factors
curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/extract-factors
-H "Content-Type: application/json"
-d '{"answers":{"age":42,"smoker":true,"exercise":"rarely","diet":"high sugar"}}'

Classify Risk
curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/classify-risk
-H "Content-Type: application/json"
-d '{"factors":["smoking","poor diet"]}'

Get Recommendations
curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/get-recommendations
-H "Content-Type: application/json"
-d '{"risk_level":"high","factors":["smoking","poor diet"]}'

Complete Analysis
curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/analyze-complete
-H "Content-Type: application/json"
-d '{"age":42,"smoker":true,"exercise":"rarely","diet":"high sugar"}'

text

---

## **Project Structure**

health-risk-profiler/
├── app.py # Flask app with all endpoints
├── config.py # Configuration variables
├── models/ # Modular pipeline components
├── utils/ # Validation and helper functions
├── uploads/ # Temporary folder for uploaded images
├── requirements.txt # Python dependencies
└── README.md # Project documentation

text

---

## **Guardrails & Error Handling**

- **Incomplete profiles** (>50% missing required fields) are rejected with:
{
"status":"incomplete_profile",
"reason":">50% fields missing: [...]"
}

text
- **Invalid or missing** image uploads return clear error JSON with HTTP 400.  
- All endpoints provide meaningful error messages and appropriate status codes.

---

## **Submission Checklist**

- [ ] Flask backend demo running locally and exposed via ngrok  
- [ ] GitHub repo with full source code and this README.md  
- [ ] Postman collection included and tested  
- [ ] Sample curl commands documented above  
- [ ] Short screen recording demonstrating all endpoints  
- [ ] Submission uploaded via Google Form: https://forms.gle/SRtHxhoBeUdJw1Pz7  
