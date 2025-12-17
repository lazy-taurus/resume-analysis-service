from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uuid
from datetime import datetime
import os
import asyncio

from llm_analyzer import analyze_resume, ResumeAnalysis
from db_utils import connect_to_mongo, close_mongo_connection, get_database

# Initialize the FastAPI application
# main.py

app = FastAPI(
    title="RESUME ANALYZER", # Change the main heading here
    description="This is a professional Python backend service that uses Gemini 2.5 Pro to execute an automated analysis pipeline for resumes.", # Change the sub-text here
    version="1.0.0",
    contact={
        "name": "Vardan Rastogi",
        "url": "https://github.com/yourusername",
    }
)

# Database collection name from env
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "analyses")


@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


class AnalysisRequest(BaseModel):
    """Input schema for the /analyze endpoint."""
    resume_text: str = Field(..., example="Vardan Rastogi\n... Java, Python...\nProject: Foodly...")
    job_description: str = Field(..., example="Backend Developer Intern\n... Knowledge of AI & ML...\nExposure in Python...")


class AnalysisResponse(BaseModel):
    id: str = Field(description="Unique ID for the analysis request.")
    status: str = Field(description="Current status of the analysis.")
    message: str = Field(description="Status message.")


@app.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Initiates the Resume Analysis Pipeline"
)
async def run_analysis(request_data: AnalysisRequest):
    # 1. Generate unique ID for the pipeline run
    analysis_id = str(uuid.uuid4())
    db = get_database()
    collection = db[COLLECTION_NAME]

    # 2. Preparation (The START of the Analysis Pipeline)
    db_document = {
        "_id": analysis_id,
        "timestamp_start": datetime.utcnow(),
        "status": "LLM_PROCESSING",
        "request_data": request_data.model_dump(),
        "analysis_result": None,
    }
    # Immediately save the request details to the DB
    await collection.insert_one(db_document)

    try:
        # 3. LLM Processing (heavy lifting) - run in thread to avoid blocking
        llm_result = await asyncio.to_thread(analyze_resume, request_data.resume_text, request_data.job_description)

        if isinstance(llm_result, dict) and "error" in llm_result:
            raise Exception(llm_result.get("details", llm_result.get("error")))

        # 4. Post-Processing & Persistence
        final_result = ResumeAnalysis(**llm_result).model_dump()

        await collection.update_one(
            {"_id": analysis_id},
            {"$set": {
                "status": "COMPLETED",
                "analysis_result": final_result,
                "timestamp_end": datetime.utcnow()
            }}
        )

        return AnalysisResponse(
            id=analysis_id,
            status="COMPLETED",
            message="Analysis complete. Result saved to database."
        )

    except Exception as e:
        error_msg = f"Analysis pipeline failed: {e}"
        await collection.update_one(
            {"_id": analysis_id},
            {"$set": {"status": "FAILED", "error_detail": error_msg, "timestamp_end": datetime.utcnow()}}
        )
        return AnalysisResponse(
            id=analysis_id,
            status="FAILED",
            message=error_msg
        )


@app.get("/status/{analysis_id}", summary="Check status or retrieve final analysis result")
async def get_analysis_result(analysis_id: str):
    db = get_database()
    collection = db[COLLECTION_NAME]

    analysis = await collection.find_one({"_id": analysis_id})

    if analysis is None:
        raise HTTPException(status_code=404, detail=f"Analysis ID '{analysis_id}' not found.")

    # Remove internal _id for return
    analysis.pop("_id", None)
    return analysis