#!/usr/bin/env python3
"""
MCP Tools-based Bug Assistant
Uses Model Context Protocol for intelligent debugging
"""

import os
import json
import ast
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash-exp")


class MCPBugAssistant:
    """Bug assistant using MCP tools"""
    
    def __init__(self):
        """Initialize the bug assistant"""
        self.client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=LOCATION
        )
        self.model_id = MODEL_NAME
        
        # Define MCP tools
        self.tools = [
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name="analyze_code_syntax",
                        description="Analyze code for syntax errors and structural issues",
                        parameters={
                            "type": "object",
                            "properties": {
                                "code": {"type": "string", "description": "Code to analyze"},
                                "language": {"type": "string", "description": "Programming language"}
                            },
                            "required": ["code", "language"]
                        }
                    ),
                    types.FunctionDeclaration(
                        name="detect_common_bugs",
                        description="Detect common bug patterns like null pointers, race conditions, etc.",
                        parameters={
                            "type": "object",
                            "properties": {
                                "code": {"type": "string", "description": "Code to check"},
                                "bug_types": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Types of bugs to check for"
                                }
                            },
                            "required": ["code"]
                        }
                    ),
                    types.FunctionDeclaration(
                        name="generate_fix",
                        description="Generate a fix for identified bugs",
                        parameters={
                            "type": "object",
                            "properties": {
                                "code": {"type": "string", "description": "Buggy code"},
                                "bug_description": {"type": "string", "description": "Description of the bug"},
                                "line_number": {"type": "integer", "description": "Line number of bug"}
                            },
                            "required": ["code", "bug_description"]
                        }
                    )
                ]
            )
        ]
    
    def _execute_tool(self, function_name: str, args: Dict[str, Any]) -> str:
        """Execute MCP tool function"""
        
        if function_name == "analyze_code_syntax":
            code = args.get("code", "")
            language = args.get("language", "python")
            
            issues = []
            
            if language == "python":
                try:
                    ast.parse(code)
                    issues.append({"type": "info", "message": "No syntax errors found"})
                except SyntaxError as e:
                    issues.append({
                        "type": "error",
                        "message": f"Syntax error at line {e.lineno}: {e.msg}",
                        "line": e.lineno
                    })
            
            return json.dumps({
                "status": "success",
                "language": language,
                "issues": issues
            })
        
        elif function_name == "detect_common_bugs":
            code = args.get("code", "")
            
            bugs = []
            
            # Check for common patterns
            if "exec(" in code or "eval(" in code:
                bugs.append({
                    "severity": "high",
                    "type": "security",
                    "message": "Dangerous use of exec/eval - code injection risk",
                    "recommendation": "Use safer alternatives or validate input"
                })
            
            if "password" in code.lower() and ("print" in code or "log" in code):
                bugs.append({
                    "severity": "high",
                    "type": "security",
                    "message": "Potential password exposure in logs",
                    "recommendation": "Never log sensitive credentials"
                })
            
            if code.count("try:") > code.count("except"):
                bugs.append({
                    "severity": "medium",
                    "type": "error_handling",
                    "message": "Incomplete exception handling",
                    "recommendation": "Add except blocks for all try statements"
                })
            
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if "TODO" in line or "FIXME" in line:
                    bugs.append({
                        "severity": "low",
                        "type": "code_quality",
                        "message": f"Unresolved TODO/FIXME at line {i}",
                        "line": i
                    })
            
            if not bugs:
                bugs.append({
                    "severity": "info",
                    "type": "info",
                    "message": "No common bug patterns detected"
                })
            
            return json.dumps({
                "status": "success",
                "bugs_found": len([b for b in bugs if b["severity"] != "info"]),
                "bugs": bugs
            })
        
        elif function_name == "generate_fix":
            code = args.get("code", "")
            bug_description = args.get("bug_description", "")
            line_number = args.get("line_number")
            
            # Generate fix suggestion
            fix_suggestion = f"""
# Original code with bug:
{code}

# Bug: {bug_description}
# Line: {line_number if line_number else 'Multiple lines'}

# Suggested fix:
# 1. Review the problematic code section
# 2. Apply proper error handling
# 3. Validate inputs
# 4. Add unit tests

# Fixed code example:
{code.replace('exec(', '# REMOVED: exec(').replace('eval(', '# REMOVED: eval(')}
"""
            
            return json.dumps({
                "status": "success",
                "fix_suggestion": fix_suggestion,
                "confidence": "high"
            })
        
        return json.dumps({"status": "error", "message": "Unknown function"})
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a file for bugs
        
        Args:
            file_path: Path to file to analyze
            
        Returns:
            Analysis results
        """
        print(f"\n🔍 Analyzing: {file_path}\n")
        
        # Read file
        try:
            with open(file_path, 'r') as f:
                code = f.read()
        except Exception as e:
            return {"error": f"Could not read file: {str(e)}"}
        
        # Determine language
        ext = Path(file_path).suffix
        language_map = {'.py': 'python', '.js': 'javascript', '.java': 'java'}
        language = language_map.get(ext, 'unknown')
        
        # Create analysis request
        request = f"""Analyze this {language} code for bugs and issues:

File: {file_path}

```{language}
{code}
```

Please identify:
1. Syntax errors
2. Common bug patterns
3. Security vulnerabilities
4. Code quality issues

Use the available tools to perform thorough analysis."""

        # Send to agent with tools
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=request,
            config=types.GenerateContentConfig(
                tools=self.tools,
                temperature=0.3,
            )
        )
        
        # Process tool calls
        results = {"file": file_path, "language": language, "tool_calls": []}
        
        # Check if there are function calls
        function_calls = []
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_calls.append(part.function_call)
        
        if function_calls:
            # Execute all function calls
            function_responses = []
            for function_call in function_calls:
                print(f"🔧 Executing: {function_call.name}")
                
                tool_result = self._execute_tool(
                    function_call.name,
                    dict(function_call.args)
                )
                
                results["tool_calls"].append({
                    "function": function_call.name,
                    "result": json.loads(tool_result)
                })
                
                function_responses.append(
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=function_call.name,
                            response={"result": tool_result}
                        )
                    )
                )
            
            # Get final analysis with all tool results
            follow_up = self.client.models.generate_content(
                model=self.model_id,
                contents=[
                    request,
                    response.candidates[0].content,
                    types.Content(parts=function_responses)
                ],
                config=types.GenerateContentConfig(temperature=0.3)
            )
            
            results["analysis"] = follow_up.text
        else:
            results["analysis"] = response.text
        
        return results
    
    def generate_report(self, results: Dict[str, Any], output_path: str = None):
        """Generate bug report"""
        if output_path is None:
            output_path = "outputs/bug_report.json"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✓ Report saved: {output_path}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("BUG ANALYSIS SUMMARY")
        print("=" * 60)
        
        for tool_call in results.get("tool_calls", []):
            result = tool_call["result"]
            if "bugs" in result:
                bugs = result["bugs"]
                high = len([b for b in bugs if b.get("severity") == "high"])
                medium = len([b for b in bugs if b.get("severity") == "medium"])
                low = len([b for b in bugs if b.get("severity") == "low"])
                
                print(f"\n🐛 Bugs found: {result.get('bugs_found', 0)}")
                print(f"   High: {high} | Medium: {medium} | Low: {low}")
                
                for bug in bugs[:5]:  # Show first 5
                    print(f"\n   [{bug['severity'].upper()}] {bug['type']}")
                    print(f"   {bug['message']}")
        
        if "analysis" in results:
            print(f"\n📝 Detailed Analysis:\n{results['analysis'][:500]}...")


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Bug Assistant")
    parser.add_argument("--file", type=str, help="File to analyze")
    parser.add_argument("--directory", type=str, help="Directory to analyze")
    parser.add_argument("--output", type=str, help="Output report path")
    
    args = parser.parse_args()
    
    assistant = MCPBugAssistant()
    
    if args.file:
        results = assistant.analyze_file(args.file)
        assistant.generate_report(results, args.output)
    elif args.directory:
        # Analyze all Python files in directory
        directory = Path(args.directory)
        for py_file in directory.rglob("*.py"):
            results = assistant.analyze_file(str(py_file))
            output = f"outputs/bug_report_{py_file.stem}.json"
            assistant.generate_report(results, output)
    else:
        # Demo with sample buggy code
        print("Running demo with sample code...\n")
        
        sample_code = """
def login(username, password):
    # TODO: Add input validation
    exec(username)  # Security issue!
    print(f"Password: {password}")  # Logging sensitive data!
    return True

def process_data(data):
    try:
        result = data / 0
    # Missing except block
    return result
"""
        
        # Save sample code
        os.makedirs("outputs", exist_ok=True)
        sample_file = "outputs/sample_buggy_code.py"
        with open(sample_file, 'w') as f:
            f.write(sample_code)
        
        results = assistant.analyze_file(sample_file)
        assistant.generate_report(results)


if __name__ == "__main__":
    main()
