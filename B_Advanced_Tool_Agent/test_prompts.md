# Agent B - Test Prompts

## Good Test Prompts (These should work well)

### 1. Code Generation Prompts

**Prompt 1: REST API with Authentication**
```
Generate a Python REST API with user authentication including login and register endpoints
```

**Expected**: Should use `generate_code_with_cli` tool and return Flask API code with JWT authentication

---

**Prompt 2: Data Processing**
```
Create a Python script to process CSV files and generate statistics
```

**Expected**: Should generate code for CSV processing

---

**Prompt 3: Web Scraper**
```
Build a Python web scraper for extracting product information from e-commerce sites
```

**Expected**: Should generate web scraping code

---

### 2. Code Analysis Prompts

**Prompt 4: Security Analysis**
```
Analyze this code for security vulnerabilities: def login(user): exec(user)
```

**Expected**: Should use `analyze_code_with_cli` tool and identify security issues

---

**Prompt 5: Performance Analysis**
```
Check this code for performance issues: for i in range(1000000): list.append(i)
```

**Expected**: Should analyze performance problems

---

### 3. Combined Prompts

**Prompt 6: Generate and Analyze**
```
Generate a Python function to validate email addresses, then analyze it for edge cases
```

**Expected**: Should use both tools - generate code first, then analyze it

---

## Quick Test Commands

### Interactive Mode
```bash
cd agent-b-gemini-cli
python3 tool_agent.py --interactive
```

Then try these one-liners:
1. `Generate a Python REST API with authentication`
2. `Create a data processing pipeline in Python`
3. `Analyze this code: def unsafe(x): eval(x)`

### Single Request Mode
```bash
python3 tool_agent.py --request "Generate a Python REST API with authentication"
```

### Demo Mode (Automated)
```bash
python3 tool_agent.py
```
This runs 3 demo requests automatically.

---

## Expected Behavior

### ✅ Good Response Pattern:
1. User makes request
2. Agent identifies it needs a tool
3. Tool is called (you see: "🔧 Tool called: generate_code_with_cli")
4. Tool executes successfully
5. Agent provides final response with code

### ❌ Bad Response Pattern (Old behavior):
1. User makes request
2. Agent asks clarifying questions
3. User provides more info
4. Agent asks more questions
5. Loop continues...

---

## Testing Checklist

- [ ] Test Prompt 1: REST API generation
- [ ] Test Prompt 2: Data processing code
- [ ] Test Prompt 3: Web scraper
- [ ] Test Prompt 4: Security analysis
- [ ] Test Prompt 5: Performance analysis
- [ ] Test Prompt 6: Combined generation + analysis
- [ ] Verify tool calls are shown
- [ ] Verify code is generated
- [ ] Verify analysis is provided

---

## Troubleshooting

**If agent asks too many questions:**
- The prompt might be too vague
- Try being more specific: "Generate Python code for X"
- Include the language explicitly

**If no tool is called:**
- Check that the request clearly asks for code generation or analysis
- Use keywords: "generate", "create", "analyze", "check"

**If you get an error:**
- Check your .env file has correct project ID
- Verify you're authenticated: `gcloud auth application-default login`
- Check API is enabled: `gcloud services list --enabled | grep aiplatform`
