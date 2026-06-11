# AI-Powered API Test Generator

🚀 **Live Demo (HTML App):** [https://api-test-generator-n5sd.onrender.com/](https://api-test-generator-n5sd.onrender.com/)

🎯 **Streamlit App:** [https://api-test-generator-mtib25qkxnte8b4pydzr9u.streamlit.app/](https://api-test-generator-mtib25qkxnte8b4pydzr9u.streamlit.app/)

🎬 **Demo Video:** [Watch on Google Drive](https://drive.google.com/file/d/1wExZe7dMkQ84SfubtWm3pxQDOFPt0Du4/view?usp=sharing)

An AI-powered tool that automatically generates **Pytest test cases** from OpenAPI/Swagger specifications using the **Groq LLaMA 3.3 70B** model.

Built by a 4-member engineering student team as part of the **AI Prototype Challenge**.

---

## 🚀 Features

- 📂 Upload OpenAPI YAML or JSON files
- 📊 View all extracted API endpoints in a clean table
- 🤖 AI automatically generates **Positive, Negative & Boundary** test cases
- ⬇️ Download generated `.py` test files directly from the browser
- 🔐 Secure API key management via `.env` file
- 🎨 Premium dark UI built with Google Stitch design

---

## 🏗️ Architecture Overview

```
User uploads OpenAPI YAML/JSON
        ↓
   parser.py reads the file
   and extracts endpoints
        ↓
   index.html displays endpoints
   in a color-coded table
        ↓
   User clicks "Generate Pytest Suite"
        ↓
   backend.py sends each endpoint
   to Groq API (LLaMA 3.3 70B)
        ↓
   AI returns Pytest code
        ↓
   Tests saved to tests/ folder
   + Download button in browser
```

---

## 📁 Project Structure

```
api-test-generator/               ← Repository Root
│
├── README.md                     # This file
├── render.yaml                   # Render deployment config
├── .gitignore                    # Git ignore rules
├── openapi.yaml                  # Sample OpenAPI spec
│
├── resume/                       # Team member resumes (PDF)
│   ├── Yashwanth_NV_Resume_Updated.pdf
│   ├── PRASANNASURIYA_Resume-v2.1.pdf
│   ├── Resume_Layasree (1).pdf
│   └── muthu resume.pdf
│
└── project/                      ← All source code lives here
    ├── app.py                    # Streamlit web application
    ├── backend.py                # FastAPI backend server
    ├── index.html                # Premium HTML frontend (Stitch UI)
    ├── parser.py                 # OpenAPI YAML/JSON parser
    ├── generator.py              # Groq AI integration
    ├── sample_openapi.yaml       # Sample OpenAPI specification
    ├── requirements.txt          # Python dependencies
    ├── prompts-notes.md          # AI prompt documentation
    ├── notes.txt                 # Development notes
    ├── AI_USAGE_NOTE.md          # AI usage report (1 page)
    │
    ├── sample_data/              # Sample input and expected outputs
    │   ├── input/
    │   │   └── sample_openapi.yaml
    │   └── output/
    │       ├── test_post_users.py
    │       └── test_post_orders.py
    │
    └── tests/                    # Generated test files + unit tests
        └── test_app.py           # Unit tests for the parser module
```

---

## ⚙️ Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/YASHWANTHTHEKING/api-test-generator.git
cd api-test-generator/project
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Your API Key
- Get a **FREE** Groq API key at: https://console.groq.com/keys
- Create a `.env` file inside the `project/` folder:
```env
GROQ_API_KEY=your_actual_key_here
```

### Step 4A: Run the HTML App (Recommended)
```bash
python backend.py
```
Open your browser at **http://localhost:8080**

### Step 4B: Run the Streamlit App
```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501**

---

## 🖥️ Run Instructions

1. Open the app in your browser.
2. Click **"Use Sample Data"** to load the built-in sample spec, OR drag and drop your own OpenAPI YAML/JSON file.
3. View the extracted endpoints in the color-coded table.
4. Click the **"⚡ Generate Pytest Suite"** button.
5. Watch the AI generate tests for each endpoint!
6. Use the **Download** or **Copy** buttons on each generated test file.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Core programming language |
| FastAPI | Backend API server |
| Streamlit | Alternative web UI |
| HTML + Tailwind CSS | Premium frontend (Stitch design) |
| Groq API (LLaMA 3.3 70B) | AI model for test generation |
| PyYAML | Parsing YAML files |
| Pandas | Displaying endpoint table |
| python-dotenv | Secure API key loading |
| Pytest | Generated test framework |
| Requests | HTTP library in generated tests |
| Render | Cloud deployment (free tier) |

---

## ⚠️ Assumptions & Limitations

- The application currently supports **OpenAPI 3.x** format only.
- The base URL in generated tests defaults to `http://localhost:8000`. Update it to match your actual API server.
- Free Groq API tier has rate limits. A **3-second delay** is added between API calls to prevent errors.
- The `.env` file must be created manually. It is excluded from GitHub for security.
- Free Render apps sleep after 15 minutes of inactivity — first load may take ~30 seconds.

---

## 👥 Team

| Name | Role | File Owned |
|---|---|---|
| Yashwanth NV | Team Leader / Frontend | `app.py`, `index.html` |
| Prasanna Suriya | AI Engineer | `generator.py` |
| Layasree | Backend / Parser | `parser.py`, `backend.py` |
| Muthuselvi | Data & Setup | `sample_openapi.yaml`, `.gitignore` |

---

## 📄 License
Open Source - Free to use for educational purposes.
