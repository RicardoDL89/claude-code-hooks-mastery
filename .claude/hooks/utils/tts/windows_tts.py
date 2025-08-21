#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

import sys
import subprocess
import random

def main():
    """
    Windows native TTS using PowerShell System.Speech
    
    Usage:
    - ./windows_tts.py                    # Uses default text
    - ./windows_tts.py "Your custom text" # Uses provided text
    """
    
    # Get text from command line argument or use default
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        completion_messages = [
            "Work complete!",
            "All done!",
            "Task finished!",
            "Job complete!",
            "Ready for next task!"
        ]
        text = random.choice(completion_messages)
    
    print("Windows TTS")
    print("=" * 15)
    print(f"Text: {text}")
    print("Speaking...")
    
    try:
        # Use PowerShell System.Speech for TTS
        powershell_cmd = f"""Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Speak('{text}')"""
        
        subprocess.run([
            "powershell", 
            "-Command", 
            powershell_cmd
        ], check=True, capture_output=True)
        
        print("Playback complete!")
        
    except subprocess.CalledProcessError as e:
        print(f"PowerShell TTS Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()