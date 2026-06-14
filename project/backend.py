"""
FastAPI Backend - AI-Powered API Test Generator
Serves the HTML frontend and handles API calls for parsing and test generation.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import sys
import json
import uuid
from datetime import datetime
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
# Paths Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR = os.path.join(BASE_DIR, "tests")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
# Ensure tests directory exists
os.makedirs(TESTS_DIR, exist_ok=True)
# Helper function to write to history.json
def add_history_entry(event_type: str, filename: str, api_title: str, version: str, endpoint_count: int, status: str):
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "filename": filename,
        "api_title": api_title,
        "version": version,
        "endpoint_count": endpoint_count,
        "status": status
    }
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            pass
    history.insert(0, entry)
    history = history[:100]  # Keep only the last 100 entries
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)
# ---- Serve the HTML frontend ----
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        return f.read()
# ---- Upload and Parse OpenAPI spec ----
@app.post("/api/upload")
async def upload_spec(file: UploadFile = File(...)):
    try:
        content = (await file.read()).decode("utf-8")
        parsed = parse_openapi_spec(content, file.filename)
        add_history_entry(
            event_type="Upload Spec",
            filename=file.filename,
            api_title=parsed.get("title", "Unknown"),
            version=parsed.get("version", "1.0"),
            endpoint_count=len(parsed.get("endpoints", [])),
            status="Parsed Successfully"
        )
        return {"success": True, "data": parsed}
    except Exception as e:
        add_history_entry(
            event_type="Upload Spec",
            filename=file.filename if file else "unknown",
            api_title="Failed",
            version="—",
            endpoint_count=0,
            status=f"Parse Error: {str(e)}"
        )
        raise HTTPException(status_code=400, detail=str(e))
# ---- Load Sample Data ----
@app.get("/api/sample")
async def load_sample():
    try:
        sample_path = os.path.join(BASE_DIR, "sample_openapi.yaml")
        if not os.path.exists(sample_path):
            raise HTTPException(status_code=404, detail="sample_openapi.yaml not found")
        with open(sample_path, "r", encoding="utf-8") as f:
            content = f.read()
        parsed = parse_openapi_spec(content, "sample_openapi.yaml")
        add_history_entry(
            event_type="Load Sample",
            filename="sample_openapi.yaml",
            api_title=parsed.get("title", "Unknown"),
            version=parsed.get("version", "1.0"),
            endpoint_count=len(parsed.get("endpoints", [])),
            status="Loaded Successfully"
        )
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
    success_count = 0
    os.makedirs(TESTS_DIR, exist_ok=True)
    
    for endpoint in request.endpoints:
        try:
            code = generate_test_code(endpoint, api_key, request.model_name)
            filepath = save_test_file(endpoint, code, output_dir=TESTS_DIR)
            results.append({
                "method": endpoint["method"],
                "path": endpoint["path"],
                "filename": os.path.basename(filepath),
                "code": code,
                "success": True
            })
            success_count += 1
        except Exception as e:
            results.append({
                "method": endpoint["method"],
                "path": endpoint["path"],
                "filename": "",
                "code": f"# Error: {str(e)}",
                "success": False
            })
    add_history_entry(
        event_type="Generate Tests",
        filename=request.model_name,
        api_title="Generated pytests",
        version="—",
        endpoint_count=len(request.endpoints),
        status=f"Generated {success_count}/{len(request.endpoints)} successfully"
    )
    return {"success": True, "results": results}
# ---- Download a generated test file ----
@app.get("/api/download/{filename}")
async def download_file(filename: str):
    filepath = os.path.join(TESTS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, filename=filename, media_type="text/x-python")
# ---- Test Suites APIs ----
@app.get("/api/test-suites")
async def list_test_suites():
    os.makedirs(TESTS_DIR, exist_ok=True)
    files = []
    try:
        for fname in os.listdir(TESTS_DIR):
            if fname.endswith(".py"):
                fpath = os.path.join(TESTS_DIR, fname)
                stat = os.stat(fpath)
                files.append({
                    "filename": fname,
                    "size": stat.st_size,
                    "created_at": stat.st_mtime
                })
        # Sort by creation time (newest first)
        files.sort(key=lambda x: x["created_at"], reverse=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"success": True, "files": files}
@app.get("/api/test-suites/{filename}")
async def get_test_suite(filename: str):
    filepath = os.path.join(TESTS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Test file not found")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        return {"success": True, "code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.delete("/api/test-suites/{filename}")
async def delete_test_suite(filename: str):
    filepath = os.path.join(TESTS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Test file not found")
    try:
        os.remove(filepath)
        return {"success": True, "message": f"Deleted {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# ---- History APIs ----
@app.get("/api/history")
async def get_history():
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            pass
    return {"success": True, "history": history}
@app.delete("/api/history/{entry_id}")
async def delete_history_entry(entry_id: str):
    if not os.path.exists(HISTORY_FILE):
        raise HTTPException(status_code=404, detail="History file not found")
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
        
        filtered_history = [entry for entry in history if entry.get("id") != entry_id]
        
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(filtered_history, f, indent=4)
        return {"success": True, "message": "History entry deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.delete("/api/history")
async def clear_history():
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        return {"success": True, "message": "History cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
