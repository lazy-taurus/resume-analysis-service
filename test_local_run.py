import os
import json
from pathlib import Path  # Added for safe path handling

# --- FIX START: Robust .env loading ---
try:
    from dotenv import load_dotenv
    # Force load .env from the same directory as this script
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path, override=True)
except Exception:
    # If python-dotenv is not installed, continue without failing.
    def load_dotenv(**kwargs):
        return None
# --- FIX END ---

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

SAMPLE_RESUME = """
Vardan Rastogi
Software engineer with 3 years experience building backend services in Python and Java.
Projects: Foodly (backend API), ML pipeline for recommendations (Python, scikit-learn), REST APIs, Docker
Skills: Python, Flask, FastAPI, SQL, PostgreSQL, Docker, CI/CD
"""

SAMPLE_JOB = """
Backend Developer Intern
We are looking for candidates with Python, experience in ML/AI pipelines, REST API development, and familiarity with TensorFlow or PyTorch.
Responsibilities: build APIs, work with data pipelines, and collaborate with ML engineers.
"""


def mocked_response():
    # A sample response that matches the ResumeAnalysis schema
    return {
        "name": "Vardan Rastogi",
        "core_skills_summary": (
            "Experienced backend developer with strong Python skills, REST API development, and database experience. "
            "Has practical exposure to ML pipelines and feature engineering through recommendation system work. "
            "Familiar with containerization (Docker) and deployment practices."
        ),
        "match_score_percent": 72,
        "missing_skills": [
            "TensorFlow",
            "PyTorch",
            "Production-grade model monitoring"
        ],
        "recommended_improvements": [
            "Add any hands-on experience with TensorFlow or PyTorch, even small projects.",
            "Include details about ML model evaluation and monitoring in production.",
            "List specific contributions to the recommendation pipeline with metrics and impact."
        ]
    }


def run_test():
    print("Running quick local test for resume analysis...")

    # Check if key is present and not a placeholder
    if not GEMINI_KEY or "YOUR_GEMINI" in GEMINI_KEY:
        print("⚠️  GEMINI_API_KEY not set or is placeholder — using mocked response.\n")
        result = mocked_response()
    else:
        # Try to call the real analyzer
        try:
            print("✅ API Key found. calling real Gemini analyzer...")
            from llm_analyzer import analyze_resume
            result = analyze_resume(SAMPLE_RESUME, SAMPLE_JOB)
        except Exception as e:
            print(f"❌ Failed to call real Gemini analyzer: {e}\nFalling back to mocked response.")
            result = mocked_response()

    print("\n--- Test Result (JSON) ---")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run_test()