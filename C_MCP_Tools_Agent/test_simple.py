#!/usr/bin/env python3
"""
Simple test for Bug Assistant
"""

import os
import sys

# Ensure we can import the module
sys.path.insert(0, os.path.dirname(__file__))

from bug_assistant import MCPBugAssistant

def test_bug_assistant():
    """Test the bug assistant with sample code"""
    print("=" * 60)
    print("Testing MCP Bug Assistant")
    print("=" * 60)
    
    # Create sample buggy code
    sample_code = """def login(username, password):
    exec(username)  # Security issue!
    print(f"Password: {password}")  # Logging sensitive data!
    return True
"""
    
    # Save to temp file
    os.makedirs("outputs", exist_ok=True)
    test_file = "outputs/test_code.py"
    with open(test_file, 'w') as f:
        f.write(sample_code)
    
    print(f"\n✓ Created test file: {test_file}")
    print(f"✓ Code to analyze:\n{sample_code}")
    
    # Initialize assistant
    print("\n🔧 Initializing Bug Assistant...")
    assistant = MCPBugAssistant()
    print("✓ Assistant initialized\n")
    
    # Analyze the file
    print("🔍 Analyzing code for bugs...\n")
    try:
        results = assistant.analyze_file(test_file)
        
        print("\n" + "=" * 60)
        print("ANALYSIS RESULTS")
        print("=" * 60)
        
        # Show tool calls
        if "tool_calls" in results:
            print(f"\n✓ Tools executed: {len(results['tool_calls'])}")
            for tool_call in results["tool_calls"]:
                print(f"  - {tool_call['function']}")
                if "bugs" in tool_call["result"]:
                    bugs = tool_call["result"]["bugs"]
                    print(f"    Found {len(bugs)} issues")
        
        # Show analysis
        if "analysis" in results:
            print(f"\n📝 Analysis Summary:")
            print("-" * 60)
            print(results["analysis"][:500])
            if len(results["analysis"]) > 500:
                print(f"\n... ({len(results['analysis']) - 500} more characters)")
        
        print("\n" + "=" * 60)
        print("✅ TEST PASSED")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_bug_assistant()
    sys.exit(0 if success else 1)
