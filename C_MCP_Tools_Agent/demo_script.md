# Demo Script: MCP Tools-based Bug Assistant

## Video Walkthrough (5-7 minutes)

### Introduction (30 seconds)
"This is Agent C - an MCP Tools-based Bug Assistant. It uses Model Context Protocol tools to analyze code, detect bugs, and suggest fixes automatically."

### MCP Tools Overview (1 minute)
Explain MCP (Model Context Protocol):
- "MCP provides a standard way to define tools for AI agents"
- "Our agent has three main tools: analyze_code_syntax, detect_common_bugs, and generate_fix"
- Show the tool definitions in the code

### Code Walkthrough (2 minutes)

Open `bug_assistant.py` and highlight:
1. **Tool Declarations**: MCP-compliant function declarations
2. **Tool Execution**: How tools are invoked and results processed
3. **Bug Detection Logic**: Pattern matching and analysis
4. **Report Generation**: Structured output with severity levels

### Live Demo (2-3 minutes)

Run with sample buggy code:
```bash
python bug_assistant.py
```

The demo will analyze code with:
- Security issues (exec/eval usage)
- Sensitive data exposure
- Missing error handling
- Code quality issues

Show the analysis process:
- Tool invocations
- Bug detection
- Severity classification

### Output Review (1 minute)

Show generated reports:
```bash
cat outputs/bug_report.json
```

Highlight:
- Bug severity levels (high/medium/low)
- Specific line numbers
- Fix recommendations
- Analysis summary

### Real File Analysis (1 minute)

Analyze a real Python file:
```bash
python bug_assistant.py --file path/to/code.py
```

Show how it works with actual code.

### Conclusion (30 seconds)
"This MCP-based agent demonstrates intelligent debugging assistance using structured tools. It can be integrated into CI/CD pipelines for automated code quality checks."
