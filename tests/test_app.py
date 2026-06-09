"""
Unit Tests for the API Test Generator Application
Tests the parser.py and generator.py modules directly (happy path coverage).

Run with: pytest tests/test_app.py -v
"""

import pytest
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import parse_openapi_spec, extract_endpoints

# ============================================================
# SAMPLE YAML for use in tests
# ============================================================

VALID_YAML = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
paths:
  /users:
    post:
      summary: Create a user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - email
              properties:
                name:
                  type: string
                email:
                  type: string
      responses:
        '201':
          description: Created
        '400':
          description: Bad Request
"""

INVALID_YAML = "this is: not: valid: yaml: {{{"

VALID_JSON = """{
  "openapi": "3.0.0",
  "info": {"title": "JSON API", "version": "2.0.0"},
  "paths": {
    "/orders": {
      "post": {
        "summary": "Create order",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": ["item_name"],
                "properties": {
                  "item_name": {"type": "string"}
                }
              }
            }
          }
        },
        "responses": {"201": {"description": "Created"}}
      }
    }
  }
}"""

# ============================================================
# PARSER TESTS
# ============================================================

class TestParser:

    def test_parse_valid_yaml(self):
        """Happy path: Valid YAML should parse successfully."""
        result = parse_openapi_spec(VALID_YAML, "test.yaml")
        assert result is not None
        assert "endpoints" in result
        assert len(result["endpoints"]) > 0

    def test_parse_valid_json(self):
        """Happy path: Valid JSON should parse successfully."""
        result = parse_openapi_spec(VALID_JSON, "test.json")
        assert result is not None
        assert "endpoints" in result

    def test_parse_extracts_title(self):
        """Happy path: Title should be correctly extracted."""
        result = parse_openapi_spec(VALID_YAML, "test.yaml")
        assert result["title"] == "Test API"

    def test_parse_extracts_version(self):
        """Happy path: Version should be correctly extracted."""
        result = parse_openapi_spec(VALID_YAML, "test.yaml")
        assert result["version"] == "1.0.0"

    def test_parse_extracts_method(self):
        """Happy path: HTTP method should be extracted as uppercase."""
        result = parse_openapi_spec(VALID_YAML, "test.yaml")
        endpoint = result["endpoints"][0]
        assert endpoint["method"] == "POST"

    def test_parse_extracts_path(self):
        """Happy path: Endpoint path should be extracted correctly."""
        result = parse_openapi_spec(VALID_YAML, "test.yaml")
        endpoint = result["endpoints"][0]
        assert endpoint["path"] == "/users"

    def test_parse_extracts_required_fields(self):
        """Happy path: Required fields should be correctly extracted."""
        result = parse_openapi_spec(VALID_YAML, "test.yaml")
        endpoint = result["endpoints"][0]
        assert "name" in endpoint["required_fields"]
        assert "email" in endpoint["required_fields"]

    def test_parse_extracts_response_codes(self):
        """Happy path: Response codes should be extracted as a list."""
        result = parse_openapi_spec(VALID_YAML, "test.yaml")
        endpoint = result["endpoints"][0]
        assert "201" in endpoint["response_codes"]
        assert "400" in endpoint["response_codes"]

    def test_parse_extracts_summary(self):
        """Happy path: Endpoint summary should be extracted."""
        result = parse_openapi_spec(VALID_YAML, "test.yaml")
        endpoint = result["endpoints"][0]
        assert endpoint["summary"] == "Create a user"

    def test_parse_invalid_yaml_raises_error(self):
        """Negative: Invalid YAML content should raise a ValueError."""
        with pytest.raises(ValueError):
            parse_openapi_spec(INVALID_YAML, "bad.yaml")

    def test_parse_empty_spec_returns_no_endpoints(self):
        """Boundary: A spec with no paths should return an empty endpoints list."""
        empty_yaml = "openapi: 3.0.0\ninfo:\n  title: Empty\n  version: 1.0.0\npaths: {}"
        result = parse_openapi_spec(empty_yaml, "empty.yaml")
        assert result["endpoints"] == []

    def test_parse_json_extracts_correctly(self):
        """Happy path: JSON format should extract the same fields as YAML."""
        result = parse_openapi_spec(VALID_JSON, "test.json")
        endpoint = result["endpoints"][0]
        assert endpoint["path"] == "/orders"
        assert endpoint["method"] == "POST"
        assert "item_name" in endpoint["required_fields"]
