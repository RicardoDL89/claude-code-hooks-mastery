#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import os
import sys
import subprocess
import json
import random
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def generate_contextual_completion_message():
    """
    Generate a contextual completion message based on recent activity.
    Uses intelligent selection from enhanced message pools.
    
    Returns:
        str: A contextual completion message
    """
    try:
        # Get engineer name if available
        engineer_name = os.getenv("ENGINEER_NAME", "").strip()
        
        # Enhanced message pools for different contexts
        general_messages = [
            "Task accomplished! Ready for your next challenge.",
            "Mission complete! Everything is set up perfectly.", 
            "Work finished! All systems are go.",
            "Job well done! Ready for the next task.",
            "Task complete! Everything is working smoothly.",
            "All wrapped up! Project finished successfully.",
            "Success! Everything is functioning correctly.",
            "Task accomplished! All requirements met.",
            "Work complete! Solution ready to use.",
            "All done! Everything configured properly.",
        ]
        
        personalized_messages = [
            f"{engineer_name}, all set!",
            f"Ready for you, {engineer_name}!",
            f"Complete, {engineer_name}!",
            f"{engineer_name}, we're done!",
            f"Task finished, {engineer_name}!",
            f"All ready, {engineer_name}!",
            f"{engineer_name}, mission accomplished!",
            f"Success, {engineer_name}!",
        ] if engineer_name else []
        
        # Combine message pools
        all_messages = general_messages + personalized_messages
        
        # Use weighted selection (30% chance for personalized if available)
        if personalized_messages and random.random() < 0.3:
            return random.choice(personalized_messages)
        else:
            return random.choice(general_messages)
        
    except Exception:
        return "Task complete! Ready for your next challenge."


def generate_completion_message():
    """
    Generate a completion message using contextual intelligence.
    
    Returns:
        str: A natural language completion message
    """
    return generate_contextual_completion_message()


def generate_agent_name():
    """
    Generate a one-word agent name using Claude Code or fallback to static names.
    
    Returns:
        str: A single-word agent name
    """
    # Fallback names for reliability
    fallback_names = [
        "Phoenix", "Sage", "Nova", "Echo", "Atlas", "Cipher", "Nexus", 
        "Oracle", "Quantum", "Zenith", "Aurora", "Vortex", "Nebula",
        "Catalyst", "Prism", "Axiom", "Helix", "Flux", "Synth", "Vertex"
    ]
    
    try:
        prompt = """Generate exactly ONE unique agent/assistant name.

Requirements:
- Single word only (no spaces, hyphens, or punctuation)  
- Abstract and memorable
- Professional sounding
- Easy to pronounce
- Similar style to: Phoenix, Sage, Nova, Echo, Atlas, Cipher, Nexus

Generate a NEW name (not from the examples). Respond with ONLY the name, nothing else.

Name:"""

        # Write prompt to temporary file
        temp_dir = Path(__file__).parent.parent.parent.parent / "temp"
        temp_dir.mkdir(exist_ok=True)
        temp_prompt_file = temp_dir / "agent_name_prompt.txt"
        
        with open(temp_prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        # Use Claude Code to generate the response
        result = subprocess.run([
            "claude", "code", "--input", str(temp_prompt_file), "--output", "-"
        ], 
        capture_output=True,
        timeout=10,  # 10-second timeout  
        text=True,
        cwd=Path(__file__).parent.parent.parent.parent
        )
        
        # Clean up temp file
        try:
            temp_prompt_file.unlink()
        except:
            pass
        
        if result.returncode == 0 and result.stdout.strip():
            # Extract and clean the name
            name = result.stdout.strip()
            # Ensure it's a single word
            name = name.split()[0] if name else "Agent"
            # Remove any punctuation
            name = ''.join(c for c in name if c.isalnum())
            # Capitalize first letter
            name = name.capitalize() if name else "Agent"
            
            # Validate it's not empty and reasonable length
            if name and 3 <= len(name) <= 20:
                return name
        
        # If Claude Code generation fails, use fallback
        raise Exception("Claude Code generation failed")
        
    except Exception:
        # Return random fallback name
        return random.choice(fallback_names)


def main():
    """Command line interface for testing."""
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--completion":
            message = generate_completion_message()
            if message:
                print(message)
            else:
                print("Error generating completion message")
        elif sys.argv[1] == "--agent-name":
            # Generate agent name (no input needed)
            name = generate_agent_name()
            print(name)
        else:
            print("Usage: ./claude_code.py --completion or ./claude_code.py --agent-name")
    else:
        print("Usage: ./claude_code.py --completion or ./claude_code.py --agent-name")


if __name__ == "__main__":
    main()