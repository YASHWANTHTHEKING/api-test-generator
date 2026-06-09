"""
Streamlit Web Application - Premium Dark UI
AI-Powered API Test Generator with TestGen AI Design
"""

import streamlit as st
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv()

from parser import parse_openapi_spec
from generator import generate_test_code, save_test_file

st.set_page_config(
    page_title="TestGen AI | API Test Generator",
    layout="wide",
    page_icon="⚡"
)

# =============================================
# INJECT CUSTOM CSS FROM STITCH DESIGN
# =============================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@100..900&family=JetBrains+Mono:wght@100..800&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>

<style>
/* ---- GLOBAL RESET ---- */
* { font-family: 'Geist', sans-serif !important; box-sizing: border-box; }

/* ---- BACKGROUND ---- */
.stApp {
    background-color: #051424 !important;
    color: #d4e4fa !important;
}
[data-testid="stAppViewContainer"] {
    background: #051424 !important;
}
[data-testid="stHeader"] {
    background: rgba(5,20,36,0.8) !important;
    backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: rgba(18,33,49,0.85) !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
}
[data-testid="stSidebar"] * {
    color: #d4e4fa !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label {
    color: #cbc3d7 !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] input {
    background: rgba(13,28,45,0.9) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #d4e4fa !important;
    border-radius: 8px !important;
}

/* ---- MAIN TITLE ---- */
h1 {
    background: linear-gradient(90deg, #d0bcff, #adc6ff) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}
h2, h3 {
    color: #d4e4fa !important;
    font-weight: 600 !important;
}

/* ---- GLASS PANELS / CONTAINERS ---- */
[data-testid="stFileUploader"],
[data-testid="stForm"],
.stExpander {
    background: rgba(18,33,49,0.7) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    padding: 8px !important;
}

/* ---- FILE UPLOADER ---- */
[data-testid="stFileUploader"] {
    background: rgba(18,33,49,0.7) !important;
    border: 2px dashed rgba(208,188,255,0.3) !important;
    border-radius: 12px !important;
    padding: 24px !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] div {
    color: #cbc3d7 !important;
}

/* ---- PRIMARY BUTTON ---- */
.stButton > button[kind="primary"],
.stButton > button {
    background: linear-gradient(90deg, #8B5CF6, #3B82F6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 32px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 0 20px rgba(139,92,246,0.3) !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 0 32px rgba(139,92,246,0.5) !important;
}

/* ---- DOWNLOAD BUTTON ---- */
.stDownloadButton > button {
    background: rgba(208,188,255,0.15) !important;
    color: #d0bcff !important;
    border: 1px solid rgba(208,188,255,0.3) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 6px 16px !important;
}

/* ---- DATAFRAME / TABLE ---- */
[data-testid="stDataFrame"] {
    background: rgba(18,33,49,0.7) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] table {
    background: transparent !important;
}
[data-testid="stDataFrame"] thead tr th {
    background: rgba(39,54,71,0.5) !important;
    color: #cbc3d7 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    border-bottom: 1px solid rgba(255,255,255,0.1) !important;
}
[data-testid="stDataFrame"] tbody tr {
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stDataFrame"] tbody tr:hover {
    background: rgba(255,255,255,0.03) !important;
}
[data-testid="stDataFrame"] tbody tr td {
    color: #d4e4fa !important;
    font-size: 13px !important;
}

/* ---- SUCCESS / ERROR MESSAGES ---- */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    background: rgba(18,33,49,0.8) !important;
}
.stSuccess {
    background: rgba(34,197,94,0.1) !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
    color: #86efac !important;
    border-radius: 10px !important;
}
.stError {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    color: #fca5a5 !important;
    border-radius: 10px !important;
}

/* ---- PROGRESS BAR ---- */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #8B5CF6, #3B82F6) !important;
    border-radius: 999px !important;
}
[data-testid="stProgress"] > div {
    background: rgba(255,255,255,0.1) !important;
    border-radius: 999px !important;
}

/* ---- EXPANDERS (generated code) ---- */
.streamlit-expanderHeader {
    background: rgba(39,54,71,0.5) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #d4e4fa !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: rgba(10,18,28,0.9) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ---- CODE BLOCKS ---- */
.stCodeBlock,
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    background: rgba(0,0,0,0.5) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}

/* ---- SELECTBOX ---- */
.stSelectbox > div > div {
    background: rgba(13,28,45,0.9) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #d4e4fa !important;
}

/* ---- ATMOSPHERIC GLOW ---- */
.stApp::before {
    content: '';
    position: fixed;
    bottom: 0; right: 0;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(208,188,255,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 25%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(59,130,246,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }

/* ---- HIDE DEFAULT STREAMLIT ELEMENTS ---- */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# =============================================
# CUSTOM HEADER
# =============================================
st.markdown("""
<div style="margin-bottom: 8px;">
    <h1 style="margin:0; padding:0;">⚡ TestGen AI</h1>
    <p style="color:#cbc3d7; margin-top:4px; font-size:15px;">
        Automatically generate Pytest test cases from OpenAPI specifications with industrial-grade precision.
    </p>
</div>
<hr style="border:none; border-top:1px solid rgba(255,255,255,0.1); margin: 16px 0 24px 0;">
""", unsafe_allow_html=True)

# =============================================
# SIDEBAR
# =============================================
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:24px;">
        <div style="font-size:20px; font-weight:700; background: linear-gradient(90deg, #d0bcff, #adc6ff);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;">QA Architect</div>
        <div style="font-size:10px; color:#cbc3d7; letter-spacing:0.1em; text-transform:uppercase; opacity:0.7;">V3.4 Stable</div>
    </div>
    """, unsafe_allow_html=True)

    env_api_key = ""
    try:
        env_api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        env_api_key = os.environ.get("GROQ_API_KEY", "")

    if env_api_key:
        api_key = env_api_key
        st.markdown("""<div style="background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.3);
            border-radius:8px; padding:8px 12px; font-size:12px; color:#86efac; margin-bottom:16px;">
            🔐 API Key Loaded Securely</div>""", unsafe_allow_html=True)
    else:
        api_key = st.text_input("Groq API Key", type="password")

    model_name = st.selectbox(
        "AI ENGINE",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )

    st.markdown("""<hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:20px 0;">""", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:11px; color:#cbc3d7; opacity:0.7; line-height:1.6;">
        Automate your QA workflow by transforming OpenAPI specs into production-ready Pytest suites using
        state-of-the-art LLMs.
    </div>
    """, unsafe_allow_html=True)

# =============================================
# MAIN LAYOUT — Upload + Status side by side
# =============================================
col1, col2 = st.columns([7, 5], gap="large")

with col1:
    st.markdown("""<div style="background:rgba(18,33,49,0.7); border:2px dashed rgba(208,188,255,0.25);
        border-radius:14px; padding:32px; text-align:center; margin-bottom:12px;">
        <div style="font-size:48px;">☁️</div>
        <h3 style="margin:8px 0 4px;">Upload OpenAPI Spec</h3>
        <p style="color:#cbc3d7; font-size:14px;">Drag and drop your YAML or JSON schema here</p>
    </div>""", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=['yaml', 'yml', 'json'], label_visibility="collapsed")

    if not uploaded_file and os.path.exists("sample_openapi.yaml"):
        if st.button("⚙️ Use Sample Data"):
            with open("sample_openapi.yaml", "r") as f:
                st.session_state['spec_content'] = f.read()
                st.session_state['filename'] = "sample_openapi.yaml"

    st.markdown("""<p style="color:#cbc3d7; font-size:11px; text-align:right; margin-top:4px;">
        ℹ️ Supported: Swagger 2.0, OpenAPI 3.0+</p>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div style="background:rgba(18,33,49,0.7); border:1px solid rgba(255,255,255,0.1);
        border-radius:14px; padding:28px; height:100%;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
            <span style="font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:#cbc3d7; font-weight:600;">Current Status</span>
            <span style="background:rgba(59,130,246,0.2); color:#adc6ff; padding:3px 10px; border-radius:999px;
                font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em;">Ready</span>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div style="background:rgba(255,255,255,0.05); padding:16px; border-radius:10px;">
                <p style="font-size:10px; text-transform:uppercase; color:#cbc3d7; margin:0 0 4px;">Parsed</p>
                <p style="font-size:28px; font-weight:700; margin:0; color:#d4e4fa;" id="ep-count">—</p>
                <p style="font-size:11px; color:#cbc3d7; margin:0;">Endpoints</p>
            </div>
            <div style="background:rgba(255,255,255,0.05); padding:16px; border-radius:10px;">
                <p style="font-size:10px; text-transform:uppercase; color:#cbc3d7; margin:0 0 4px;">Model</p>
                <p style="font-size:14px; font-weight:700; margin:0; color:#d0bcff;">LLaMA 3.3</p>
                <p style="font-size:11px; color:#cbc3d7; margin:0;">70B Versatile</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    generate_clicked = st.button("⚡ Generate Pytest Suite", type="primary")

# =============================================
# PARSE AND DISPLAY
# =============================================
if uploaded_file is not None:
    st.session_state['spec_content'] = uploaded_file.getvalue().decode("utf-8")
    st.session_state['filename'] = uploaded_file.name

if 'spec_content' in st.session_state:
    try:
        parsed_data = parse_openapi_spec(st.session_state['spec_content'], st.session_state['filename'])
        st.success(f"✅ Loaded **{parsed_data['title']}** (v{parsed_data['version']}) — {len(parsed_data['endpoints'])} endpoints found")

        st.markdown("""<div style="display:flex; justify-content:space-between; align-items:center; margin:24px 0 12px;">
            <h3 style="margin:0;">Analyzed Endpoints</h3>
        </div>""", unsafe_allow_html=True)

        table_data = []
        for ep in parsed_data['endpoints']:
            method = ep['method']
            color_map = {"GET": "#22c55e", "POST": "#3b82f6", "PUT": "#eab308", "DELETE": "#ef4444", "PATCH": "#f97316"}
            color = color_map.get(method, "#cbc3d7")
            table_data.append({
                "Method": method,
                "Path": ep['path'],
                "Summary": ep['summary'],
                "Required Fields": ", ".join(ep['required_fields']) if ep['required_fields'] else "None",
                "Responses": ", ".join(ep['response_codes'])
            })

        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # =============================================
        # GENERATE
        # =============================================
        if generate_clicked:
            if not api_key:
                st.error("⚠️ Please enter your Groq API key in the sidebar.")
            else:
                total = len(parsed_data['endpoints'])
                progress_bar = st.progress(0)
                status_text = st.empty()

                for idx, ep in enumerate(parsed_data['endpoints']):
                    status_text.markdown(f"""<div style="color:#cbc3d7; font-size:13px; margin:8px 0;">
                        🔄 Generating test for <b style='color:#d0bcff;'>{ep['method']} {ep['path']}</b>...</div>""",
                        unsafe_allow_html=True)
                    try:
                        code = generate_test_code(ep, api_key, model_name)
                        filepath = save_test_file(ep, code, output_dir="tests")

                        with st.expander(f"✅  {ep['method']} {ep['path']} → {os.path.basename(filepath)}", expanded=True):
                            st.download_button(
                                label=f"⬇️ Download {os.path.basename(filepath)}",
                                data=code,
                                file_name=os.path.basename(filepath),
                                mime="text/x-python",
                                key=f"dl_{idx}"
                            )
                            st.code(code, language='python')

                        if idx < total - 1:
                            time.sleep(3)
                    except Exception as e:
                        st.error(f"❌ Failed for {ep['path']}: {str(e)}")

                    progress_bar.progress((idx + 1) / total)

                status_text.markdown("""<div style="color:#86efac; font-size:13px; font-weight:600;">
                    ✅ Generation complete! All tests saved to <code>tests/</code></div>""", unsafe_allow_html=True)
                st.balloons()

    except Exception as e:
        st.error(f"❌ Error parsing file: {str(e)}")
