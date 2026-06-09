"""
Streamlit Web Application
This is the main entry point for the College Project API Test Generator.
It provides a UI to upload OpenAPI files, extract endpoints into a table,
and generate Pytest suites using Gemini AI.
"""

import streamlit as st
import pandas as pd
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our custom modules
from parser import parse_openapi_spec
from generator import generate_test_code, save_test_file

# Set up the Streamlit page configuration
st.set_page_config(page_title="API Test Generator", layout="wide")

st.title("AI-Powered API Test Generator")

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("Configuration")
    
    env_api_key = os.environ.get("GROQ_API_KEY", "")
    
    if env_api_key:
        api_key = env_api_key
    else:
        api_key = st.text_input("Groq API Key", type="password")
        
    model_name = st.selectbox(
        "AI Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )

uploaded_file = st.file_uploader("Upload OpenAPI YAML or JSON file", type=['yaml', 'yml', 'json'])

# Provide a button to load the sample file if the user doesn't want to upload one
if not uploaded_file and os.path.exists("sample_openapi.yaml"):
    if st.button("Use Sample Data"):
        with open("sample_openapi.yaml", "r") as f:
            st.session_state['spec_content'] = f.read()
            st.session_state['filename'] = "sample_openapi.yaml"

# If the user uploads a file, read its contents
if uploaded_file is not None:
    st.session_state['spec_content'] = uploaded_file.getvalue().decode("utf-8")
    st.session_state['filename'] = uploaded_file.name

# --- STEP 2: PARSE AND DISPLAY DATA ---
if 'spec_content' in st.session_state:
    try:
        # Call our parser module to extract the endpoints
        parsed_data = parse_openapi_spec(st.session_state['spec_content'], st.session_state['filename'])
        st.success(f"Successfully loaded '{parsed_data['title']}' (v{parsed_data['version']}).")
        
        # Format the endpoints into a Pandas DataFrame for a clean table view
        table_data = []
        for ep in parsed_data['endpoints']:
            table_data.append({
                "Method": ep['method'],
                "Path": ep['path'],
                "Summary": ep['summary'],
                "Required Fields": ", ".join(ep['required_fields']) if ep['required_fields'] else "None",
                "Expected Responses": ", ".join(ep['response_codes'])
            })
            
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True) # Display the table in Streamlit
            
        # --- STEP 3: GENERATE TESTS ---
        if st.button("Generate Pytest Suite", type="primary"):
            if not api_key:
                st.error("Please enter your Groq API key in the sidebar before generating tests.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                total = len(parsed_data['endpoints'])
                
                # Loop through each endpoint and generate a test
                for idx, ep in enumerate(parsed_data['endpoints']):
                    status_text.text(f"Generating tests for {ep['method']} {ep['path']}...")
                    
                    try:
                        # 1. Ask the LLM to write the code
                        code = generate_test_code(ep, api_key, model_name)
                        
                        # 2. Save it to a local folder (tests/)
                        filepath = save_test_file(ep, code, output_dir="tests")
                        
                        # 3. Create an expander UI to show the code and the Download button
                        with st.expander(f"✅ Generated: {ep['method']} {ep['path']} (Saved to {filepath})", expanded=True):
                            # Provide a download button for this specific file
                            st.download_button(
                                label="⬇️ Download " + os.path.basename(filepath),
                                data=code,
                                file_name=os.path.basename(filepath),
                                mime="text/x-python",
                                key=f"download_{idx}"
                            )
                            # Show the syntax-highlighted code
                            st.code(code, language='python')
                            
                        # Add a 3-second delay to prevent hitting free-tier API rate limits
                        if idx < total - 1:
                            time.sleep(3)
                            
                    except Exception as e:
                        st.error(f"Failed to generate tests for {ep['path']}: {str(e)}")
                        
                    progress_bar.progress((idx + 1) / total)
                    
                status_text.text("Generation complete! All files have been saved to the 'tests/' folder.")
                st.balloons() # Fun animation to show completion!
                
    except Exception as e:
        st.error(f"Error parsing file: {str(e)}")
