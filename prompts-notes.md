# Prompt Documentation - AI-Powered API Test Generator
## College Project | Team: YASHWANTHTHEKING

This file documents all the key prompts used during the development of this project
with the help of AI coding assistants (Google Antigravity / Claude).

---

## 1. Project Scaffolding Prompt
Used to generate the initial project structure and file layout.

```
Build a simple AI-Powered API Test Generator using Python.
- Use Streamlit for the frontend
- Accept OpenAPI YAML or JSON file uploads
- Parse all endpoints (path, method, required fields, response codes)
- Use Google Gemini / Groq LLM to generate Pytest test cases
- Generate: Positive Tests, Negative Tests, Boundary Tests
- Save generated tests to a local tests/ folder
- Project structure:
    app.py, parser.py, generator.py, requirements.txt, sample_openapi.yaml
```

---

## 2. OpenAPI Parser Prompt
Used to generate the parser.py logic.

```
Write a Python function called parse_openapi_spec(content, filename).
- Accept both YAML and JSON formats
- Extract from each endpoint:
  - HTTP method (GET, POST, PUT, DELETE, PATCH)
  - URL path
  - Summary
  - Required fields from requestBody schema
  - Expected response codes
- Return a dictionary with title, version, and list of endpoints
- Add beginner-friendly comments explaining each step
```

---

## 3. LLM Test Generator Prompt (System Prompt sent to Groq/LLaMA)
This is the actual system prompt injected into the Groq API call inside generator.py.

```
You are an expert QA Engineer and Python SDET.
Your task is to generate robust, production-ready API test cases
using pytest and requests.

Requirements for generated tests:
1. Include imports for pytest and requests.
2. Generate the following types of tests:
   A. Positive Tests: Valid request payload returning expected success code (200/201)
   B. Negative Tests:
      - Missing required fields
      - Invalid data types
      - Invalid email format (if email is required)
   C. Boundary Tests:
      - Empty strings
      - Maximum length values
      - Null values
3. Use http://localhost:8000 as the base URL.
4. Add clear assertions (assert response.status_code == ...).
5. Provide Python code ONLY. Do not wrap code in markdown blocks.
```

---

## 4. Streamlit UI Prompt
Used to generate the frontend app.py.

```
Write a Streamlit web app that:
- Has a file uploader for OpenAPI YAML/JSON files
- Has a sidebar with an API key input (hidden/password type) and model selector
- Loads the API key from a .env file automatically using python-dotenv
- Shows the extracted endpoints in a pandas DataFrame table
- Has a "Generate Pytest Suite" button
- Shows a progress bar while generating
- Displays each generated test in an expandable code block
- Adds a download button for each generated .py file
- Shows balloons animation on completion
```

---

## 5. Sample OpenAPI Spec Prompt
Used to generate the sample_openapi.yaml test file.

```
Write an OpenAPI 3.0 YAML specification for a simple API with two endpoints:
1. POST /users - Creates a new user. Required fields: name (string), email (email format).
   Returns 201 on success, 400 on bad request.
2. POST /orders - Creates a new order. Required fields: user_id (integer), item_name (string),
   quantity (integer, minimum 1). Returns 201 on success, 400 on bad request.
```

---

## 6. Security & Git Setup Prompt
Used to generate the .env and .gitignore files.

```
Create a .env file with a placeholder GROQ_API_KEY variable.
Create a .gitignore file that:
- Ignores .env and .env.* files (to protect API keys)
- Ignores Python __pycache__ and *.pyc files
- Ignores virtual environment folders (venv/, .venv/)
- Ignores .pytest_cache/ and .streamlit/ folders
```

---

## Tools & Technologies Used
| Tool | Purpose |
|------|---------|
| Python 3.x | Core programming language |
| Streamlit | Web UI framework |
| Groq API (LLaMA 3.3 70B) | AI model for test generation |
| PyYAML | Parsing YAML OpenAPI specs |
| Pandas | Displaying endpoint table in UI |
| python-dotenv | Securely loading API keys from .env |
| Pytest | Generated test framework |
| Requests | HTTP library used in generated tests |
| Git + GitHub | Version control and collaboration |
