"""
AI Test Generator
This module interacts with the Google Gemini AI to dynamically write
Python Pytest code based on the API endpoints we extracted.
"""

import os
from groq import Groq

# The SYSTEM_PROMPT tells the AI *how* it should act and what rules to follow.
SYSTEM_PROMPT = """You are an expert QA Engineer and Python SDET.
Your task is to generate robust, production-ready API test cases using `pytest` and `requests`.

Requirements for generated tests:
1. Include imports for `pytest` and `requests`.
2. Generate the following types of tests:
   A. Positive Tests: Valid request payload returning expected success code (e.g., 200/201).
   B. Negative Tests: 
      - Missing required fields
      - Invalid data types
      - Invalid email format (if email is required)
   C. Boundary Tests:
      - Empty strings
      - Maximum length values
      - Null values
3. Use `http://localhost:8000` as the base URL.
4. Add clear assertions (`assert response.status_code == ...`).
5. Provide Python code ONLY. Do not wrap code in markdown blocks (like ```python).
"""

# The USER_PROMPT_TEMPLATE gives the AI the specific data for one endpoint.
USER_PROMPT_TEMPLATE = """Generate pytest code for the following API endpoint:

Method: {method}
Path: {path}
Summary: {summary}

Required Fields:
{required_fields}

Expected Response Codes:
{response_codes}

Full Schema Details:
{full_schema}

Generate the complete Python test file now.
"""

def generate_test_code(endpoint: dict, api_key: str, model_name: str) -> str:
    """
    Takes a single endpoint dictionary, formats the prompt, and calls Gemini.
    """
    if not api_key:
        raise ValueError("API key is missing.")
        
    # Initialize the Groq Client with the user's API key
    client = Groq(api_key=api_key)
    
    # Fill in the blanks of our prompt template with the endpoint data
    prompt = USER_PROMPT_TEMPLATE.format(
        method=endpoint["method"],
        path=endpoint["path"],
        summary=endpoint["summary"],
        required_fields=endpoint["required_fields"],
        response_codes=endpoint["response_codes"],
        full_schema=endpoint.get("full_schema", {})
    )
    
    try:
        # Call the AI model via Groq
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            # Temperature 0.2 makes the AI more deterministic and less "creative" (better for coding)
            temperature=0.2
        )
        
        # Sometimes the AI wraps code in markdown (```python ... ```). We strip that out.
        code = response.choices[0].message.content
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
            
        return code.strip()
        
    except Exception as e:
        # If the API fails (e.g., quota exceeded, bad key), return a graceful error message as a Python comment
        return f"# Error generating test: {str(e)}\n\nimport pytest\n\ndef test_error():\n    pytest.fail('Test generation failed due to API error.')"

def save_test_file(endpoint: dict, code: str, output_dir: str = "tests"):
    """
    Saves the generated string of code into a physical .py file.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Create safe filename based on the endpoint path
    safe_path = endpoint["path"].replace("/", "_").strip("_")
    if not safe_path:
        safe_path = "root"
    
    filename = f"test_{endpoint['method'].lower()}_{safe_path}.py"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
        
    return filepath
