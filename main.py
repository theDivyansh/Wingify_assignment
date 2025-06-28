from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from typing import Dict, Any

from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, verification, nutrition_analysis, exercise_planning

app = FastAPI(title="Blood Test Report Analyser")


def validate_file(file: UploadFile):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

async def run_crew(query: str, file_path: str = "data/sample.pdf") -> Dict[str, Any]:
    """Run the full medical crew."""
    medical_crew = Crew(
        agents=[verifier, doctor, nutritionist, exercise_specialist],
        tasks=[verification, help_patients, nutrition_analysis, exercise_planning],
        process=Process.sequential,
        verbose=True,
        memory=True,
        max_rpm=100,
    )

    inputs = {
        'query': query,
        'file_path': file_path
    }

    result = await medical_crew.kickoff(inputs)
    return result


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Blood Test Report Analyser API is running",
        "status": "healthy",
    }

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(..., description="Blood test report PDF file"),
    query: str = Form(default="Summarise my Blood Test Report")
):
    validate_file(file)
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        with open(file_path, "wb") as f:
            f.write(content)

        query = query.strip() or "Summarise my Blood Test Report"
        response = await run_crew(query=query, file_path=file_path)

        return {
            "message": "Blood test report analyzed successfully",
            "query": query,
            "file_processed": file.filename,
            "analysis": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as cleanup_error:
                print(f"Warning: Failed to cleanup file {file_path}: {cleanup_error}")

## Quick analysis Route -> Bonus point
@app.post("/quick-analyze")
async def quick_analyze(
    file: UploadFile = File(..., description="Blood test report PDF file"),
    query: str = Form(default="Give me a quick summary", description="Quick analysis request")
):
    validate_file(file)
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        with open(file_path, "wb") as f:
            f.write(content)

        query = query.strip() or "Give me a quick summary of blood test results"

        quick_crew = Crew(
            agents=[verifier, doctor],
            tasks=[verification, help_patients],
            process=Process.sequential,
            verbose=False,
        )

        inputs = {'query': query, 'file_path': file_path}
        result = await quick_crew.kickoff(inputs)

        return {
            "status": "success",
            "message": "Quick analysis completed",
            "query": query,
            "file_processed": file.filename,
            "analysis": str(result)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in quick analysis: {str(e)}")
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
