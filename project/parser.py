"""
OpenAPI Specification Parser
This module reads an uploaded OpenAPI JSON or YAML file and extracts
the important API endpoints to be used for test generation.
"""

import yaml
import json
from typing import Dict, Any

def parse_openapi_spec(content: str, filename: str) -> Dict[str, Any]:
    """
    Reads the raw file content and converts it into a Python dictionary.
    Supports both JSON and YAML formats.
    """
    try:
        # Check the file extension to decide how to parse it
        if filename.endswith(".json"):
            spec = json.loads(content)
        else:
            spec = yaml.safe_load(content)
            
        # Once parsed into a dictionary, extract just the endpoints we care about
        return extract_endpoints(spec)
    except Exception as e:
        # If the file is invalid, raise a clear error message
        raise ValueError(f"Failed to parse OpenAPI spec: {str(e)}")

def extract_endpoints(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Loops through the OpenAPI paths and extracts only the relevant data
    (like HTTP methods, required fields, and expected response codes).
    """
    endpoints = []
    
    # Get the "paths" dictionary from the OpenAPI spec
    paths = spec.get("paths", {})
    
    # Loop through each URL path (e.g., '/users', '/orders')
    for path, path_data in paths.items():
        if not isinstance(path_data, dict):
            continue
            
        # Loop through each HTTP method under the path (e.g., 'get', 'post')
        for method, operation in path_data.items():
            if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                continue
                
            # --- Extract Required Fields ---
            # We look inside the requestBody -> content -> application/json -> schema
            required_fields = []
            request_body = operation.get("requestBody", {})
            content = request_body.get("content", {})
            app_json = content.get("application/json", {})
            schema = app_json.get("schema", {})
            if "required" in schema:
                required_fields = schema["required"]
                
            # --- Extract Expected Responses ---
            # We just get the keys from the 'responses' dictionary (like '200', '201')
            responses = operation.get("responses", {})
            response_codes = list(responses.keys())
                
            # Append the cleaned-up data to our endpoints list
            endpoints.append({
                "method": method.upper(),
                "path": path,
                "summary": operation.get("summary", "No summary provided"),
                "required_fields": required_fields,
                "response_codes": response_codes,
                # We also keep the raw schema in case the LLM needs more details
                "full_schema": schema
            })
            
    # Also extract the API title and version for the UI
    info = spec.get("info", {})
    return {
        "title": info.get("title", "Unknown API"),
        "version": info.get("version", "1.0"),
        "endpoints": endpoints
    }
