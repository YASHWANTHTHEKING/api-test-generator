"""
FastAPI Backend - AI-Powered API Test Generator
Serves the HTML frontend and handles API calls for parsing and test generation.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os
import sys

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import parse_openapi_spec
from generator import generate_test_code, save_test_file

app = FastAPI(title="TestGen AI Backend")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Serve the HTML frontend ----
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# ---- Upload and Parse OpenAPI spec ----
@app.post("/api/upload")
async def upload_spec(file: UploadFile = File(...)):
    try:
        content = (await file.read()).decode("utf-8")
        parsed = parse_openapi_spec(content, file.filename)
        return {"success": True, "data": parsed}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---- Load Sample Data ----
@app.get("/api/sample")
async def load_sample():
    try:
        sample_path = "sample_openapi.yaml"
        if not os.path.exists(sample_path):
            raise HTTPException(status_code=404, detail="sample_openapi.yaml not found")
        with open(sample_path, "r") as f:
            content = f.read()
        parsed = parse_openapi_spec(content, "sample_openapi.yaml")
        return {"success": True, "data": parsed}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---- Generate Tests ----
class GenerateRequest(BaseModel):
    endpoints: List[dict]
    model_name: str = "llama-3.3-70b-versatile"

@app.post("/api/generate")
async def generate_tests(request: GenerateRequest):
    # Load API key from environment
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.environ.get("GROQ_API_KEY", "")
        except:
            pass

    if not api_key:
        raise HTTPException(status_code=401, detail="GROQ_API_KEY not set in .env file")

    results = []
    for endpoint in request.endpoints:
        try:
            code = generate_test_code(endpoint, api_key, request.model_name)
            filepath = save_test_file(endpoint, code, output_dir="tests")
            results.append({
                "method": endpoint["method"],
                "path": endpoint["path"],
                "filename": os.path.basename(filepath),
                "code": code,
                "success": True
            })
        except Exception as e:
            results.append({
                "method": endpoint["method"],
                "path": endpoint["path"],
                "filename": "",
                "code": f"# Error: {str(e)}",
                "success": False
            })

    return {"success": True, "results": results}

# ---- Download a generated test file ----
@app.get("/api/download/{filename}")
async def download_file(filename: str):
    filepath = os.path.join("tests", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, filename=filename, media_type="text/x-python")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
