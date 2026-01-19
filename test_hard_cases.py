from agent.graph import run_agent
import json

# Hard test cases to test self-correction capability
hard_test_cases = [
    # Case 1: Typos and inconsistent formatting
    "Jhn is 30 yrs old from new yorK, wrks at gogle, salary $150,000",
    
    # Case 2: Age written as word
    "Sarah is twenty-eight years old from London, works at Amazon, salary 95000",
    
    # Case 3: Missing fields
    "Bob is 45 from Boston",
    
    # Case 4: Extra noise and special characters
    "Person: Dave @@ Age: 32!!! City: San Francisco... Company: Netflix $$$ Salary: 180K",
    
    # Case 5: Multiple sentences and context
    "I am Emma, born in 1995 (so I'm about 30 years old). Currently residing in Sydney, Australia. Working at Tesla as an engineer earning 200k AUD.",
    
    # Case 6: Abbreviations and shorthand
    "Mr. Raj, 35yo from BNG, eng @ MSFT, sal 120L (in INR)",
    
    # Case 7: Unusual age format
    "Michael is in his mid-forties, lives in Miami, employed by Apple",
    
    # Case 8: Non-standard salary format
    "Lisa (age 29) from Chicago @ IBM - income 110K annually",
    
    # Case 9: Non-standard salary format
    "Priya, age 26, from Bangalore, works at Google, earns 150000",
    
    # Case 10: Very messy with extra info
    "Hey! My name is Alex. I'm 33 years of age. I'm based in Seattle (Washington). My job is with Microsoft. They pay me about 200k per year. I love it here!",
]

print("=" * 70)
print("HARD EXAMPLES TEST - Self-Correcting AI Agent")
print("=" * 70)
print()

success_count = 0
failed_count = 0

for i, test_text in enumerate(hard_test_cases, 1):
    print("Test {}: {}...".format(i, test_text[:60]))
    print("-" * 70)
    
    result = run_agent(test_text)
    
    if result['status'] == 'success':
        data = result['data']
        attempts = result.get('attempts', 0)
        attempt_msg = "(FIRST TRY)" if attempts == 0 else "(CORRECTED {} TIME{})".format(attempts, 'S' if attempts > 1 else '')
        
        print("[SUCCESS] {} ".format(attempt_msg))
        print("  Name: {}".format(data['name']))
        print("  Age: {}".format(data['age']))
        print("  City: {}".format(data['city']))
        print("  Company: {}".format(data['company']))
        print("  Salary: {}".format(data['salary_lpa']))
        success_count += 1
    else:
        print("[FAILED]")
        print("  Status: {}".format(result['status']))
        print("  Error: {}".format(result.get('error', 'Unknown error')))
        print("  Attempts: {}".format(result.get('attempts', 0)))
        failed_count += 1
    
    print()

print("=" * 70)
print("SUMMARY: {} Success | {} Failed".format(success_count, failed_count))
print("Success Rate: {}/{} ({}%)".format(success_count, len(hard_test_cases), 100*success_count//len(hard_test_cases)))
print("=" * 70)
