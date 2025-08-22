#!/usr/bin/env python3
import sys
import os

# Add the LLM utils directory to path
sys.path.append('.claude/hooks/utils/llm')

try:
    import claude_code
    message = claude_code.generate_completion_message()
    print(f"Generated message: {message}")
    print("Success!")
except Exception as e:
    print(f"Error: {e}")