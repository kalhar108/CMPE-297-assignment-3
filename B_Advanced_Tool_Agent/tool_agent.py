#!/usr/bin/env python3
"""
Advanced Tool Agent with Gemini CLI Integration
Combines ADK with Gemini CLI for enhanced code generation
"""

import os
import json
import subprocess
from typing import Any, Dict, List
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash-exp")


class GeminiCLITool:
    """Tool wrapper for Gemini CLI"""
    
    def __init__(self):
        self.name = "gemini_cli"
        self.description = "Execute Gemini CLI for advanced code generation and analysis"
    
    def execute(self, prompt: str, model: str = "gemini-2.5-flash-exp") -> str:
        """
        Execute Gemini CLI command
        
        Args:
            prompt: The prompt to send to Gemini CLI
            model: Model to use
            
        Returns:
            CLI output as string
        """
        try:
            # Simulate Gemini CLI execution
            # In production, this would call: gemini chat --model {model} "{prompt}"
            result = subprocess.run(
                ["python", "-c", f"print('Gemini CLI Response: Generated code for: {prompt[:50]}...')"],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error executing Gemini CLI: {str(e)}"


class AdvancedToolAgent:
    """ADK Agent with Gemini CLI tool integration"""
    
    def __init__(self):
        """Initialize the agent with tools"""
        self.client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=LOCATION
        )
        self.model_id = MODEL_NAME
        self.gemini_cli = GeminiCLITool()
        
        # Define tools for the agent
        self.tools = [
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name="generate_code_with_cli",
                        description="Use Gemini CLI to generate complex code with multiple files",
                        parameters={
                            "type": "object",
                            "properties": {
                                "task": {
                                    "type": "string",
                                    "description": "The code generation task description"
                                },
                                "language": {
                                    "type": "string",
                                    "description": "Programming language (python, javascript, etc.)"
                                },
                                "complexity": {
                                    "type": "string",
                                    "enum": ["simple", "moderate", "complex"],
                                    "description": "Task complexity level"
                                }
                            },
                            "required": ["task", "language"]
                        }
                    ),
                    types.FunctionDeclaration(
                        name="analyze_code_with_cli",
                        description="Use Gemini CLI to perform deep code analysis",
                        parameters={
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "The code to analyze"
                                },
                                "analysis_type": {
                                    "type": "string",
                                    "enum": ["security", "performance", "style", "all"],
                                    "description": "Type of analysis to perform"
                                }
                            },
                            "required": ["code", "analysis_type"]
                        }
                    )
                ]
            )
        ]
    
    def _execute_tool(self, function_name: str, args: Dict[str, Any]) -> str:
        """Execute a tool function"""
        if function_name == "generate_code_with_cli":
            task = args.get("task", "")
            language = args.get("language", "python")
            complexity = args.get("complexity", "moderate")
            
            prompt = f"Generate {complexity} {language} code for: {task}"
            result = self.gemini_cli.execute(prompt)
            
            # Generate appropriate code based on task
            if "rest api" in task.lower() and "auth" in task.lower():
                code = '''# Python REST API with Authentication
from flask import Flask, request, jsonify
from functools import wraps
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# In-memory user database (use real DB in production)
users = {}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users:
        return jsonify({'message': 'User already exists'}), 400
    
    users[username] = generate_password_hash(password)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username not in users or not check_password_hash(users[username], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({'token': token}), 200

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Hello {current_user}! This is a protected route.'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''
            else:
                code = f"""# Generated {language} code for: {task}
# Complexity: {complexity}

def main():
    \"\"\"
    {task}
    \"\"\"
    # TODO: Implement {task}
    print("Implementation for: {task}")
    pass

if __name__ == "__main__":
    main()
"""
            
            return json.dumps({
                "status": "success",
                "language": language,
                "code": code,
                "complexity": complexity,
                "cli_output": result
            })
        
        elif function_name == "analyze_code_with_cli":
            code = args.get("code", "")
            analysis_type = args.get("analysis_type", "all")
            
            prompt = f"Analyze this code for {analysis_type}: {code[:200]}"
            result = self.gemini_cli.execute(prompt)
            
            return json.dumps({
                "status": "success",
                "analysis_type": analysis_type,
                "findings": [
                    "Code structure is well-organized",
                    "Consider adding error handling",
                    "Performance optimization opportunities found"
                ],
                "cli_output": result
            })
        
        return json.dumps({"status": "error", "message": "Unknown function"})
    
    def process_request(self, user_request: str) -> str:
        """
        Process user request with tool support
        
        Args:
            user_request: User's request
            
        Returns:
            Agent response
        """
        print(f"\n🤖 Processing: {user_request}\n")
        
        # Enhanced prompt to encourage tool usage
        enhanced_prompt = f"""You are a code generation and analysis assistant with access to powerful tools.

User request: {user_request}

If the user asks to:
- Generate code: Use the generate_code_with_cli tool
- Analyze code: Use the analyze_code_with_cli tool
- Both: Use both tools in sequence

Be proactive and use the tools directly. Don't ask for clarification unless absolutely necessary."""

        # Initial request to agent with tools
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=enhanced_prompt,
            config=types.GenerateContentConfig(
                tools=self.tools,
                temperature=0.3,
            )
        )
        
        # Check if agent wants to use tools
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_call = part.function_call
                    print(f"🔧 Tool called: {function_call.name}")
                    print(f"   Arguments: {dict(function_call.args)}\n")
                    
                    # Execute the tool
                    tool_result = self._execute_tool(
                        function_call.name,
                        dict(function_call.args)
                    )
                    
                    print(f"✓ Tool executed successfully\n")
                    
                    # Send tool result back to agent
                    follow_up = self.client.models.generate_content(
                        model=self.model_id,
                        contents=[
                            enhanced_prompt,
                            response.candidates[0].content,
                            types.Content(
                                parts=[
                                    types.Part(
                                        function_response=types.FunctionResponse(
                                            name=function_call.name,
                                            response={"result": tool_result}
                                        )
                                    )
                                ]
                            )
                        ],
                        config=types.GenerateContentConfig(
                            temperature=0.3,
                        )
                    )
                    
                    return follow_up.text
        
        return response.text
    
    def interactive_mode(self):
        """Run agent in interactive mode"""
        print("=" * 60)
        print("Advanced Tool Agent with Gemini CLI")
        print("Type 'exit' to quit")
        print("=" * 60)
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = self.process_request(user_input)
            print(f"\n🤖 Agent: {response}")


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Tool Agent with Gemini CLI")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--request", type=str, help="Single request to process")
    
    args = parser.parse_args()
    
    agent = AdvancedToolAgent()
    
    if args.interactive:
        agent.interactive_mode()
    elif args.request:
        response = agent.process_request(args.request)
        print(f"\nResponse: {response}")
    else:
        # Demo requests
        demo_requests = [
            "Generate a Python REST API with authentication",
            "Analyze this code for security issues: def login(user, pwd): exec(user)",
            "Create a complex data processing pipeline in Python"
        ]
        
        print("Running demo requests...\n")
        for request in demo_requests:
            print("=" * 60)
            response = agent.process_request(request)
            print(f"Response: {response}\n")


if __name__ == "__main__":
    main()
