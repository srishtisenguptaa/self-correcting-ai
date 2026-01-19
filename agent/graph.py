from langchain_ollama import OllamaLLM
from agent.extractor import extract_data
from agent.validator import validate_data
from agent.corrector import correct_data
import json
import re

# Initialize Ollama LLM (local, no API key needed)
llm = OllamaLLM(
    model="qwen2.5:3b-instruct-q4_k_m",  # Using available model
    temperature=0
)

def extract_json(text):
    """Extract JSON from text, handling markdown code blocks"""
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()
    
    # Try to parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON object in text
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise

def run_agent(raw_text: str):
    """
    Main workflow: Extract → Validate → Correct (if validation fails)
    """
    try:
        # Step 1: Extract
        extracted_str = extract_data(llm, raw_text)
        extracted_json = extract_json(extracted_str)
        
        # Step 2: Validate
        is_valid, validated_data, error = validate_data(extracted_json)
        
        if is_valid:
            return {"status": "success", "data": validated_data.dict()}
        
        # Step 3: Self-correct (retry loop)
        max_retries = 3
        for attempt in range(max_retries):
            corrected_str = correct_data(llm, raw_text, extracted_json, error)
            corrected_json = extract_json(corrected_str)
            
            is_valid, validated_data, error = validate_data(corrected_json)
            if is_valid:
                return {"status": "success", "data": validated_data.dict(), "attempts": attempt + 1}
        
        return {"status": "failed", "error": str(error), "attempts": max_retries}
    
    except Exception as e:
        return {"status": "error", "error": str(e)}