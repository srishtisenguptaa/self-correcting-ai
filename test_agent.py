from agent.graph import run_agent

# Test cases
test_cases = [
    'John is 30 years old from New York, works at Google, salary 150000',
    'My name is Sarah, age 28, city is London, company is Amazon',
    'Ram aged 35 from Bangalore working at Microsoft earning 120000 rupees'
]

print('=== Self-Correcting AI Agent Test ===\n')
for i, test in enumerate(test_cases, 1):
    print(f'Test {i}: {test}')
    result = run_agent(test)
    if result['status'] == 'success':
        print(f"✓ Success: {result['data']}")
    else:
        print(f"✗ Result: {result}")
    print()
