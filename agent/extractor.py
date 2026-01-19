# LLM extraction logic
def extract_data(llm, raw_text: str):
    prompt = f"""Extract user profile data from the text below.
Return ONLY a JSON object (no markdown, no extra text) with these fields:
- name (string)
- age (integer, 18-100)
- city (string)
- company (string or null)
- salary_lpa (number or null)

Text: {raw_text}

Return only valid JSON, nothing else."""

    response = llm.invoke(prompt)
    return response.strip()
