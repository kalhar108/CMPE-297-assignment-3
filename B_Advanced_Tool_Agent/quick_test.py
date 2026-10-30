#!/usr/bin/env python3
"""
Quick test script for Agent B
"""

from tool_agent import AdvancedToolAgent

def test_agent():
    """Run quick tests"""
    agent = AdvancedToolAgent()
    
    print("=" * 70)
    print("AGENT B - QUICK TEST")
    print("=" * 70)
    
    test_cases = [
        {
            "name": "Test 1: REST API Generation",
            "prompt": "Generate a Python REST API with authentication"
        },
        {
            "name": "Test 2: Data Processing",
            "prompt": "Create Python code to process CSV files"
        },
        {
            "name": "Test 3: Security Analysis",
            "prompt": "Analyze this code for security: def login(user): exec(user)"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"{test['name']}")
        print(f"{'='*70}")
        print(f"Prompt: {test['prompt']}\n")
        
        try:
            response = agent.process_request(test['prompt'])
            print(f"✅ Success!")
            print(f"\nResponse preview (first 500 chars):")
            print("-" * 70)
            print(response[:500])
            if len(response) > 500:
                print(f"\n... ({len(response) - 500} more characters)")
            print("-" * 70)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        if i < len(test_cases):
            input("\nPress Enter to continue to next test...")
    
    print(f"\n{'='*70}")
    print("ALL TESTS COMPLETE")
    print(f"{'='*70}")

if __name__ == "__main__":
    test_agent()
