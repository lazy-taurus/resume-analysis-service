from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from llm_analyzer import analyze_resume, ResumeAnalysis

# Initialize the FastAPI application
app = FastAPI(
    title="IBM Internship Resume Analyzer API",
    description="A Python backend service using Gemini for structured resume analysis."
)

class AnalysisRequest(BaseModel):
    """Input schema for the /analyze endpoint."""
    resume_text: str = Field(..., example="Vardan Rastogi\n... Java, Python...\nProject: Foodly...")
    job_description: str = Field(..., example="Backend Developer Intern\n... Knowledge of AI & ML...\nExposure in Python...")

@app.post(
    "/analyze",
    response_model=ResumeAnalysis,
    summary="Run a structured resume analysis against a job description"
)
def run_analysis(request_data: AnalysisRequest):
    """
    Takes resume text and job description and calls the Gemini LLM 
    to return a structured analysis and match score.
    """
    if not request_data.resume_text or not request_data.job_description:
        raise HTTPException(status_code=400, detail="Both resume text and job description are required.")

    # Call the core LLM function from llm_analyzer.py
    result = analyze_resume(request_data.resume_text, request_data.job_description)

    # CHECK FOR ERRORS BEFORE RETURNING
    # If we return the dict directly, Pydantic tries to validate it against ResumeAnalysis immediately.
    # We need to catch the error dict first.
    if "error" in result:
        # Raise the specific error from the analyzer
        raise HTTPException(
            status_code=500, 
            detail=result.get("details", result.get("error", "Unknown error from Gemini."))
        )

    # If no error, return the valid result
    return result