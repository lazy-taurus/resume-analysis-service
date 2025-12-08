# Resume Analysis Service

A minimal FastAPI service that calls the Google Gemini (genai) SDK to analyze resumes and produce a structured JSON result.

Quick start (Windows PowerShell):

```powershell
cd "v:/github/resume parser/resume-analysis-service"
python -m venv venv
.\venv\Scripts\Activate.ps1  # or use .\venv\Scripts\activate
pip install -r requirements.txt
# Create a .env file with your GEMINI_API_KEY (see .env.example)
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs` to interact with the `/analyze` endpoint.

Files created:
- `llm_analyzer.py` — Gemini client + analyze function
- `main.py` — FastAPI app and `/analyze` endpoint
- `.env` — API key placeholder (ignored by git)
- `requirements.txt` — dependencies
