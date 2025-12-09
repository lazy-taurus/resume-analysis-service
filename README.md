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
- `db_utils.py` — MongoDB async helpers
- `tests/test_analyzer.py` — pytest unit with mocked GenAI client
- `run_pipeline_test.py` — integration run to persist results to MongoDB
- `.env` — local environment variables (ignored by git)
- `requirements.txt` — dependencies

**Project Title:** LLM-Powered Resume Analysis Pipeline

**Technologies:** Python, FastAPI, Motor (async MongoDB), Pydantic, google-genai (Gemini), Docker, Docker Compose, Pytest

System Architecture (Analysis Pipeline Execution):
- Client sends `POST /analyze` with `resume_text` and `job_description`.
- Server assigns a unique `analysis_id` and saves initial document with status `LLM_PROCESSING`.
- The server calls `analyze_resume()` (Gemini) to generate a structured JSON response.
- The final validated result is saved into MongoDB and the DB document is updated with status `COMPLETED`.
- Clients can poll `GET /status/{analysis_id}` to retrieve the analysis and status.

Docker & Local Deployment
-------------------------
We include a `Dockerfile` and `docker-compose.yml` so you can run the API and a local MongoDB together.

Build and run locally with Docker Compose:

```powershell
cd "v:/github/resume parser/resume-analysis-service"
docker-compose up --build
```

This binds the API to port `8000` on your machine and starts a local MongoDB on port `27017`.

Environment variables
---------------------
- `GEMINI_API_KEY` — your Gemini/Google API key (keep secret)
- `MONGO_URL` — MongoDB connection string (use Atlas for production)
- `MONGO_DB_NAME` — database name (default `resume_analysis_db`)
- `COLLECTION_NAME` — collection to store analyses (default `analyses`)

Running tests
-------------
Run the unit test suite (mocked GenAI client):

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

API Endpoints
-------------
- `POST /analyze` — Start the analysis pipeline. Returns an `id` and status.
- `GET /status/{analysis_id}` — Retrieve status and stored analysis result.

Deployment
----------
For production, build and push your Docker image to a registry (or connect your GitHub repo to Render). Configure your cloud host to set environment variables securely and use MongoDB Atlas for a managed database. Start command for services that expect `$PORT`:

```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Security / Notes
----------------
- Never commit `GEMINI_API_KEY` or other secrets to source control. Use `.env` locally and a secret manager in CI/production.
- Consider adding request size limits, authentication, and rate limiting before exposing the API publicly.

