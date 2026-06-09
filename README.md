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

---

## 🏗️ Architecture Overview

```
User uploads OpenAPI YAML/JSON
        ↓
   parser.py reads the file
   and extracts endpoints
        ↓
   app.py displays endpoints
   in a Pandas table
        ↓
   User clicks "Generate Tests"
        ↓
   generator.py sends each endpoint
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
api-test-generator/
│
├── app.py                  # Streamlit web application (Frontend)
├── parser.py               # OpenAPI YAML/JSON parser
├── generator.py            # Groq AI integration and test generator
├── sample_openapi.yaml     # Sample OpenAPI specification for testing
├── requirements.txt        # Python dependencies
├── prompts-notes.md        # AI prompt documentation
├── notes.txt               # Development notes
├── .env                    # API key (NOT committed to GitHub)
├── .gitignore              # Git ignore rules
│
├── sample_data/            # Sample input and expected output files
│   ├── input/
│   │   └── sample_openapi.yaml
│   └── output/
│       ├── test_post_users.py
│       └── test_post_orders.py
│
└── tests/                  # Generated test files land here
    └── test_app.py         # Unit tests for our application
```

---

## ⚙️ Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/YASHWANTHTHEKING/api-test-generator.git
cd api-test-generator
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Your API Key
- Get a **FREE** Groq API key at: https://console.groq.com/keys
- Open the `.env` file and replace the placeholder:
```env
GROQ_API_KEY=your_actual_key_here
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`.

---

## 🖥️ Run Instructions

1. Open the app in your browser.
2. Click **"Use Sample Data"** to load the built-in sample spec, OR upload your own OpenAPI YAML/JSON file.
3. View the extracted endpoints in the table.
4. Click the **"Generate Pytest Suite"** button.
5. Watch the AI generate tests for each endpoint!
6. Download the test files using the **Download** buttons.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Core programming language |
| Streamlit | Web UI |
| Groq API (LLaMA 3.3 70B) | AI model for test generation |
| PyYAML | Parsing YAML files |
| Pandas | Displaying endpoint table |
| python-dotenv | Secure API key loading |
| Pytest | Generated test framework |
| Requests | HTTP library in generated tests |

---

## ⚠️ Assumptions & Limitations

- The application currently supports **OpenAPI 3.x** format only.
- The base URL in generated tests defaults to `http://localhost:8000`. Update it to match your actual API server.
- Free Groq API tier has rate limits. A **3-second delay** is added between API calls to prevent errors.
- The `.env` file must be created manually. It is excluded from GitHub for security.
- The app generates tests based on the spec structure. If your spec is incomplete, the generated tests may not cover all edge cases.

---

## 👥 Team

| Name | Role | File Owned |
|---|---|---|
| Yashwanth NV | Team Leader / Frontend | `app.py` |
| Prasanna Suriya | AI Engineer | `generator.py` |
| Layasree | Backend / Parser | `parser.py` |
| Muthuselvi | Data & Setup | `sample_openapi.yaml`, `.gitignore` |

---

## 📄 License
Open Source - Free to use for educational purposes.
