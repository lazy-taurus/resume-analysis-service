from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, Field
import json
import time

# --- 1. Load Environment Variables Safely ---
# Locate the .env file in the same directory as this script
env_path = Path(__file__).parent / '.env'

# FORCE override system variables with the .env file
# This is crucial to stop the "API Key Expired" loop
load_dotenv(dotenv_path=env_path, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Use the models we verified work
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash") 
GEMINI_FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash")

# --- 2. Initialize Client ---
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    print("⚠️ CRITICAL WARNING: GEMINI_API_KEY is missing from .env file.")
    client = None

# --- 3. Define Output Schema ---
class ResumeAnalysis(BaseModel):
    """Schema for the structured analysis result using Pydantic."""
    name: str = Field(description="The full name of the candidate found in the resume.")
    core_skills_summary: str = Field(description="A 3-sentence summary of the candidate's core technical skills relevant to the job.")
    match_score_percent: int = Field(description="An estimated match percentage (0-100) for the candidate against the provided Job Description.")
    missing_skills: list[str] = Field(description="A list of 3 specific technical skills mentioned in the job description that are NOT found in the resume.")
    recommended_improvements: list[str] = Field(description="A list of 3 specific, actionable suggestions for improving the resume for this job.")


# --- 4. Main Analysis Function ---
def analyze_resume(resume_text: str, job_description: str) -> dict:
    """Sends the resume and job description to the Gemini LLM for structured analysis."""
    
    if not client:
        return {
            "error": "Configuration Error", 
            "details": "API Key missing. Please check your .env file."
        }

    system_instruction = """
    You are an expert Resume Analyzer AI. 
    Analyze the candidate's resume against the job description.
    You MUST output valid JSON matching the schema provided.
    """

    user_prompt = f"""
    --- CANDIDATE RESUME ---
    {resume_text}

    --- JOB DESCRIPTION ---
    {job_description}
    """

    def _call_model(model_name: str):
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResumeAnalysis,
            system_instruction=system_instruction,
        )
        return client.models.generate_content(
            model=model_name,
            contents=[user_prompt],
            config=config,
        )

    # Try primary model, then fallback
    last_error = None
    for model_to_try in (GEMINI_MODEL, GEMINI_FALLBACK_MODEL):
        try:
            # print(f"DEBUG: Analyzing with {model_to_try}...") 
            response = _call_model(model_to_try)
            
            # Extract text carefully
            text = response.text
            
            # Parse JSON
            return json.loads(text)

        except Exception as e:
            last_error = e
            error_msg = str(e)
            print(f"⚠️ Error with {model_to_try}: {error_msg}")
            
            # If it's a 404 (Model not found) or 429 (Quota), try the next model
            if "404" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                 time.sleep(1)
                 continue
            else:
                # If it's a weird error, break and fail
                break

    return {
        "error": "Analysis Failed", 
        "details": f"All models failed. Last error: {str(last_error)}"
    }