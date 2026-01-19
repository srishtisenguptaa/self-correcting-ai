# Retry + self-correction logic
def correct_data(llm, raw_text, previous_output, error):
    prompt = f"""You previously extracted this data from text:
{previous_output}

But it failed validation with this error:
{error}

Fix the JSON output so it passes validation and matches the schema.
Return ONLY valid JSON with fields: name, age, city, company, salary_lpa
Do not include markdown, backticks, or explanations."""

    response = llm.invoke(prompt)
    return response.strip()
