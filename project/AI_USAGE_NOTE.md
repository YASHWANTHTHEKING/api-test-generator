# AI Usage Note
## Project: AI-Powered API Test Generator
## Team: YASHWANTHTHEKING | Date: June 2026

---

## 1. What AI Helped With

### Code Generation
- AI generated the **entire project structure** from a single prompt describing the requirements.
- AI wrote `parser.py` — a clean, modular function that reads both YAML and JSON OpenAPI specs and extracts endpoints, required fields, and response codes.
- AI wrote `generator.py` — including the system prompt design, Groq API integration, and markdown stripping logic.
- AI wrote `app.py` — the complete Streamlit UI including file upload, Pandas table display, progress bar, expandable code blocks, and download buttons.
- AI generated the `sample_openapi.yaml` file with realistic `/users` and `/orders` endpoints.
- AI generated all documentation files: `README.md`, `prompts-notes.md`, `notes.txt`, `.gitignore`.

### Debugging
- When the app threw `ImportError: cannot import name 'save_test_file'`, AI identified that the function was accidentally omitted during a refactor and instantly patched it.
- When Gemini API returned `404 NOT_FOUND` errors, AI diagnosed the issue as incorrect model name strings and switched the backend to **Groq** which uses stable, free model names.
- When Groq returned `model_decommissioned` errors for `llama3-8b-8192`, AI updated all model references to the correct current names (`llama-3.3-70b-versatile`, `llama-3.1-8b-instant`).

### Architecture Decisions
- AI recommended switching from a complex **React + FastAPI + Docker** architecture to a simple **Streamlit + Python** architecture, making the project far more beginner-friendly and easier to explain.
- AI recommended using `python-dotenv` for secure API key management instead of hardcoding keys in the UI.

---

## 2. What AI Got Wrong

| Issue | What Went Wrong | How We Fixed It |
|---|---|---|
| Wrong model names | AI used `gemini-1.5-flash` and `gemini-2.0-flash-exp` which returned 404 errors | Switched to Groq API with stable model names |
| Missing function | After rewriting `generator.py`, AI forgot to include the `save_test_file()` function | AI caught the error from the traceback and added the missing function |
| Decommissioned models | AI suggested `llama3-8b-8192` which had been retired by Groq | Updated to `llama-3.1-8b-instant` |
| Over-engineering | First version used React + FastAPI + Docker which was too complex | AI simplified to pure Python + Streamlit |
| Unnecessary UI clutter | The UI had too many headers, success boxes and labels | Cleaned up after user flagged it |

---

## 3. Best Prompts Used

### Prompt 1 — Architecture Decision (Most Effective)
```
project/
│
├── app.py
├── parser.py
├── generator.py
├── requirements.txt
├── sample_openapi.yaml
└── tests/

Use this file structure and change everything.
```
**Why it worked:** Giving the AI a concrete file structure instead of a vague description 
made it immediately understand the desired architecture and rewrite everything correctly.

### Prompt 2 — LLM System Prompt Design
```
Generate the following types of tests:
A. Positive Tests: Valid request payload
B. Negative Tests: Missing required fields, Invalid data types, Invalid email format
C. Boundary Tests: Empty strings, Maximum length values, Null values
Provide Python code ONLY. Do not wrap code in markdown blocks.
```
**Why it worked:** Explicitly listing A, B, C test categories with examples forced the AI 
to structure its output in exactly the way we needed.

### Prompt 3 — Debugging by Error Message
```
ImportError: cannot import name 'save_test_file' from 'generator'
```
**Why it worked:** Pasting the raw error message directly gave the AI the exact context 
needed to identify and fix the bug in one shot without any explanation.

---

## 4. Overall AI Contribution Summary

| Area | % AI Contributed |
|---|---|
| Code Writing | ~90% |
| Debugging | ~80% |
| Documentation | ~95% |
| Architecture Design | ~70% |
| Prompt Engineering | ~50% (Team guided the AI) |

The team's role was primarily in **guiding the AI** with the right prompts, 
**testing the output**, identifying failures, and **presenting the solution**.

---

*This document was prepared as part of the mandatory AI Usage Note requirement 
for the AI Prototype Challenge submission.*
