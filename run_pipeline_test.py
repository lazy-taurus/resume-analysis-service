import asyncio
import uuid
from datetime import datetime
from db_utils import connect_to_mongo, close_mongo_connection, get_database
from llm_analyzer import analyze_resume, ResumeAnalysis
import os


async def run_test():
    await connect_to_mongo()
    try:
        db = get_database()
        collection = db[os.getenv("COLLECTION_NAME", "analyses")]

        analysis_id = str(uuid.uuid4())
        req = {
            "resume_text": "Vardan Rastogi\nSoftware engineer with 3 years experience building backend services in Python and Java.",
            "job_description": "Backend Developer Intern\nWe are looking for candidates with Python and ML/AI experience."
        }

        doc = {
            "_id": analysis_id,
            "timestamp_start": datetime.utcnow(),
            "status": "LLM_PROCESSING",
            "request_data": req,
            "analysis_result": None,
        }

        await collection.insert_one(doc)

        # Call analyzer in thread to avoid blocking
        llm_result = await asyncio.to_thread(analyze_resume, req["resume_text"], req["job_description"])

        if isinstance(llm_result, dict) and "error" in llm_result:
            await collection.update_one({"_id": analysis_id}, {"$set": {"status": "FAILED", "error_detail": llm_result.get("details")}})
            print("LLM call failed:", llm_result.get("details"))
        else:
            final = ResumeAnalysis(**llm_result).model_dump()
            await collection.update_one({"_id": analysis_id}, {"$set": {"status": "COMPLETED", "analysis_result": final, "timestamp_end": datetime.utcnow()}})
            stored = await collection.find_one({"_id": analysis_id})
            # Remove internal _id and print saved document keys
            stored.pop("_id", None)
            print("Stored document:")
            print(stored)

    finally:
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(run_test())
