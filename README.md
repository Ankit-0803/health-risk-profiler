# AI-Powered Health Risk Profiler Backend

## Overview
This project provides a Flask-based API backend that processes health survey data via **text** or **scanned images**. It uses **OCR** for image parsing, extracts critical health risk factors, classifies risk levels, and generates personalized recommendations. The backend is exposed publicly via an **ngrok** tunnel for easy remote testing and demo.

## Live Demo URL (ngrok)
https://saul-repoussa-articulately.ngrok-free.dev  
_All API requests should be sent to the above base URL._

## Features
- Supports survey input as **JSON (text)** or **uploaded image (OCR)**
- Accurate extraction and normalization of health factors
- **Risk classification** with **confidence scoring** and **rationale**
- Tailored **non-diagnostic** recommendations
- Robust **guardrails** for incomplete or invalid inputs
- Clear **JSON** responses with meaningful error messages

## Setup Instructions

**Prerequisites**  
- Python 3.8+  
- Tesseract OCR installed and in your system PATH  
- ngrok for public tunneling

**Installation**  
1. Clone repo  
   `git clone https://github.com/yourusername/health-risk-profiler.git`  
   `cd health-risk-profiler`  
2. Create virtual environment  
   `python -m venv venv`  
3. Activate venv  
   Windows: `venv\Scripts\activate`  
   Linux/Mac: `source venv/bin/activate`  
4. Install dependencies  
   `pip install -r requirements.txt`

**Run the Backend Locally**  
`python app.py`

**Expose via ngrok**  
In a new terminal:  
`ngrok http 8080`  

## API Endpoints

| Endpoint               | Method | Description                                |
|------------------------|--------|--------------------------------------------|
| `/`                    | GET    | Health check, service status               |
| `/parse-text`          | POST   | Parse survey data JSON                     |
| `/parse-image`         | POST   | Parse uploaded survey image (OCR)          |
| `/extract-factors`     | POST   | Extract risk factors from survey answers   |
| `/classify-risk`       | POST   | Classify risk based on factors             |
| `/get-recommendations` | POST   | Generate recommendations                   |
| `/analyze-complete`    | POST   | Complete pipeline: parse → classify → recommend |

## Sample curl Requests
Replace base URL if ngrok changes  
curl -X GET https://saul-repoussa-articulately.ngrok-free.dev/

curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/parse-text
-H "Content-Type: application/json"
-d '{"age":42,"smoker":true,"exercise":"rarely","diet":"high sugar"}'

curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/parse-image
-F "image=@survey-form.jpg"

curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/extract-factors
-H "Content-Type: application/json"
-d '{"answers":{"age":42,"smoker":true,"exercise":"rarely","diet":"high sugar"}}'

curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/classify-risk
-H "Content-Type: application/json"
-d '{"factors":["smoking","poor diet"]}'

curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/get-recommendations
-H "Content-Type: application/json"
-d '{"risk_level":"high","factors":["smoking","poor diet"]}'

curl -X POST https://saul-repoussa-articulately.ngrok-free.dev/analyze-complete
-H "Content-Type: application/json"
-d '{"age":42,"smoker":true,"exercise":"rarely","diet":"high sugar"}'


## Guardrails & Error Handling
- **Incomplete profiles** (>50% missing required fields) return  
{"status":"incomplete_profile","reason":">50% fields missing: [...]"}
- **Invalid or missing** image uploads return clear error JSON (HTTP 400)
- All endpoints return meaningful error messages and appropriate status codes

## Submission Checklist
- [ ] Flask backend demo running locally and exposed via ngrok  
- [ ] GitHub repo with full source code and README.md  
- [ ] Postman collection included and tested  
- [ ] Sample curl commands documented above  
- [ ] Short screen recording demonstrating all endpoints  
- [ ] Submission uploaded via Google Form: https://forms.gle/SRtHxhoBeUdJw1Pz7
