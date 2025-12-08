from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import json

# Load environment variables from the .env file
load_dotenv()

# Initialize the Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class ResumeAnalysis(BaseModel):
    """Schema for the structured analysis result using Pydantic."""
    name: str = Field(description="The full name of the candidate found in the resume.")
    core_skills_summary: str = Field(description="A 3-sentence summary of the candidate's core technical skills relevant to the job.")
    match_score_percent: int = Field(description="An estimated match percentage (0-100) for the candidate against the provided Job Description, focusing on AI/ML/Python skills.")
    missing_skills: list[str] = Field(description="A list of 3 specific technical skills mentioned in the job description that are NOT found in the resume.")
    recommended_improvements: list[str] = Field(description="A list of 3 specific, actionable suggestions for improving the resume for this job, based on the missing skills.")


def analyze_resume(resume_text: str, job_description: str) -> dict:
    """Sends the resume and job description to the Gemini LLM for structured analysis."""

    # 1. System Instruction: Guiding the LLM's role and behavior
    system_instruction = f"""
    You are an expert Backend Developer Intern Resume Analyzer AI, specialized in IBM job descriptions. 
    Your task is to analyze the provided resume text and score it against the provided Job Description. 
    You MUST strictly adhere to the exact JSON output schema provided in the configuration. 
    Be critical but fair, paying special attention to Python, AI/ML, and API experience.
    """

    # 2. User Prompt: Combining the inputs the LLM needs to process
    user_prompt = f"""
    --- CANDIDATE RESUME TEXT ---
    {resume_text}

    --- TARGET JOB DESCRIPTION ---
    {job_description}
    """

    try:
        # 3. Configuration: Ensuring the output is structured JSON matching the Pydantic model
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResumeAnalysis, # Uses the Pydantic class to enforce schema
            system_instruction=system_instruction
        )

        # 4. Call the Gemini API
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[user_prompt],
            config=config,
        )

        # 5. Return the JSON result
        # The SDK response structure may vary; assume textual JSON is available on `response.text`.
        return json.loads(response.text)

    except Exception as e:
        # Handle API errors gracefully
        print(f"Gemini API Error: {e}")
        return {"error": "Failed to get response from Gemini.", "details": str(e)}
