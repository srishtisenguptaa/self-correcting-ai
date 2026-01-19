# Self-Correcting AI

A framework for building self-correcting AI agents that validate, extract, and automatically correct their outputs using LLM self-correction.

## Features

- **Data Extraction**: Extract structured data from unstructured text using LLM
- **Validation**: Validate extracted data against Pydantic schemas
- **Self-Correction**: Automatically retry and correct failed validations using the LLM
- **Ollama Integration**: Uses local Ollama models (no API keys needed)

## Project Structure

- `app.py` - Streamlit UI
- `api.py` - FastAPI server
- `agent/` - Core agent logic
  - `graph.py` - Main orchestration workflow
  - `extractor.py` - LLM data extraction
  - `validator.py` - Pydantic validation
  - `corrector.py` - Self-correction logic
- `storage/` - Data persistence
  - `db.py` - Database operations
- `models/` - Data models
  - `schemas.py` - Pydantic UserProfile schema

## Setup

### Prerequisites
- Python 3.14+
- Ollama installed and running (`ollama serve`)
- Model downloaded: `ollama pull qwen2.5:3b-instruct-q4_k_m`

### Installation

1. Create virtual environment (already done in `.venv/`)
2. Install dependencies:
   ```powershell
   C:/Projects/self_correcting_ai/.venv/Scripts/python.exe -m pip install -r requirements.txt
   ```

## Usage

### Option 1: Direct Python (Recommended for testing)

```powershell
cd C:\Projects\self_correcting_ai
C:/Projects/self_correcting_ai/.venv/Scripts/python.exe test_agent.py
```

Example output:
```
Test 1: John is 30 years old from New York, works at Google, salary 150000
✓ Success: {'name': 'John', 'age': 30, 'city': 'New York', 'company': 'Google', 'salary_lpa': 150000.0}
```

### Option 2: FastAPI + Streamlit

**Terminal 1 - Start API Server:**
```powershell
cd C:\Projects\self_correcting_ai
C:/Projects/self_correcting_ai/.venv/Scripts/python.exe -m uvicorn api:app --port 8000
```

**Terminal 2 - Start Streamlit UI:**
```powershell
cd C:\Projects\self_correcting_ai
C:/Projects/self_correcting_ai/.venv/Scripts/streamlit run app.py
```

Then open http://localhost:8501 and paste your data.

## How It Works

1. **Extract**: LLM extracts data from raw text into JSON
2. **Validate**: Pydantic validates against UserProfile schema
3. **Correct**: If validation fails, LLM self-corrects and retries (up to 3 times)
4. **Return**: Returns validated data or error message

## Example

Input:
```
"John is 30 years old from New York, works at Google, salary 150000"
```

Output:
```json
{
  "status": "success",
  "data": {
    "name": "John",
    "age": 30,
    "city": "New York",
    "company": "Google",
    "salary_lpa": 150000.0
  }
}
```

## Configuration

Edit `agent/graph.py` to change:
- **Model**: Change `"qwen2.5:3b-instruct-q4_k_m"` to any Ollama model
- **Temperature**: Adjust for more/less creative responses
- **Max Retries**: Change `max_retries = 3` for correction attempts

