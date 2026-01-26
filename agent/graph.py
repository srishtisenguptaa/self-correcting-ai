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

def detect_uncertainty(raw_text: str):
    """
    Detects ambiguity / approximation in user input.
    Returns a penalty score between 0 and 0.4
    """
    text = raw_text.lower()

    approx_keywords = [
        "around", "approx", "approximately",
        "early", "mid", "late",
        "about", "roughly", "nearly",
        "range", "between", "to"
    ]

    penalty = 0.0

    for word in approx_keywords:
        if word in text:
            penalty += 0.1

    # Cap penalty so confidence doesn't drop too much
    return min(penalty, 0.4)


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
    Returns: status, data, retries, attempts, and confidence score
    """
    try:
        # Detect uncertainty upfront
        uncertainty_penalty = detect_uncertainty(raw_text)

        # Step 1: Extract
        extracted_str = extract_data(llm, raw_text)
        extracted_json = extract_json(extracted_str)

        # Step 2: Validate
        is_valid, validated_data, error = validate_data(extracted_json)

        if is_valid:
            confidence = 1.0 - uncertainty_penalty

            return {
                "status": "success",
                "data": validated_data.dict(),
                "retries": 0,
                "attempts": 1,
                "confidence": round(max(0.5, confidence), 2)
            }

        # Step 3: Self-correct (retry loop)
        max_retries = 3
        for attempt in range(max_retries):
            corrected_str = correct_data(llm, raw_text, extracted_json, error)
            corrected_json = extract_json(corrected_str)

            is_valid, validated_data, error = validate_data(corrected_json)
            if is_valid:
                # Retry penalty + uncertainty penalty
                confidence = 1.0
                confidence -= uncertainty_penalty
                confidence -= (attempt + 1) * 0.15  # retry penalty

                return {
                    "status": "success",
                    "data": validated_data.dict(),
                    "retries": attempt + 1,
                    "attempts": attempt + 2,
                    "confidence": round(max(0.5, confidence), 2)
                }

        return {
            "status": "failed",
            "error": str(error),
            "retries": max_retries,
            "attempts": max_retries,
            "confidence": 0.0
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "retries": 0,
            "confidence": 0.0
        }
