# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a demonstration repository for **Claude Code Hooks Mastery** - showcasing advanced Claude Code hooks, sub-agents, output styles, and status lines. The project uses UV single-file scripts for hook implementations and demonstrates all 8 hook lifecycle events.

## Development Commands

### Running Scripts
```bash
# Execute UV single-file Python scripts
uv run apps/hello.py
uv run .claude/hooks/user_prompt_submit.py --help

# Run hooks directly (used by Claude Code automatically)
uv run .claude/hooks/pre_tool_use.py
uv run .claude/hooks/stop.py --chat
uv run .claude/status_lines/status_line_v3.py
```

### Testing Hook Functionality
```bash
# View hook execution logs
cat logs/user_prompt_submit.json | jq '.'
cat logs/pre_tool_use.json | jq '.'
cat logs/post_tool_use.json | jq '.'

# Test status line directly
uv run .claude/status_lines/status_line_v3.py

# Check session data
ls .claude/data/sessions/
```

## Project Architecture

### Hook System Structure
The project implements all 8 Claude Code hook types using UV single-file scripts:

- **UserPromptSubmit** (`.claude/hooks/user_prompt_submit.py`) - Prompt validation, logging, context injection
- **PreToolUse** (`.claude/hooks/pre_tool_use.py`) - Security blocking, command validation
- **PostToolUse** (`.claude/hooks/post_tool_use.py`) - Result logging, transcript conversion
- **Notification** (`.claude/hooks/notification.py`) - TTS notifications
- **Stop** (`.claude/hooks/stop.py`) - AI-generated completion messages with TTS
- **SubagentStop** (`.claude/hooks/subagent_stop.py`) - Sub-agent completion notifications
- **PreCompact** (`.claude/hooks/pre_compact.py`) - Transcript backup before compaction
- **SessionStart** (`.claude/hooks/session_start.py`) - Development context loading

### Sub-Agent System
Comprehensive collection of specialized sub-agents in `.claude/agents/`:

- **Meta-Agent** (`meta-agent.md`) - Creates new sub-agents from descriptions
- **Crypto Analysis Suite** (`crypto/`) - Market analysis, price tracking, investment strategies
- **Work Completion Summary** (`work-completion-summary.md`) - Audio summaries via TTS
- **AI Research Specialist** (`llm-ai-agents-and-eng-research.md`) - Latest AI/ML developments

### Utility Architecture
- **TTS Providers** (`.claude/hooks/utils/tts/`) - ElevenLabs, OpenAI, pyttsx3 fallback
- **LLM Integrations** (`.claude/hooks/utils/llm/`) - OpenAI, Anthropic, Ollama completion services
- **Session Management** (`.claude/data/sessions/`) - Agent naming, prompt history, custom metadata

### Configuration Files
- `.claude/settings.json` - Main configuration with hook permissions and commands
- `.claude/output-styles/` - Custom response formatting (genui, table-based, yaml-structured, etc.)
- `.claude/status_lines/` - Terminal status displays (v1-v4 with increasing functionality)
- `.claude/commands/` - Custom slash commands for specialized workflows

### Logging System
All hook events are logged as JSON to `logs/` directory:
- `user_prompt_submit.json` - User prompt submissions with validation
- `pre_tool_use.json` - Tool use events with security blocking
- `post_tool_use.json` - Tool completion events
- `notification.json` - Notification events
- `stop.json` - Stop events with completion messages
- `chat.json` - Readable conversation transcript (most recent session only)

## Key Features

### Security Enhancements
- Command validation blocks dangerous operations (`rm -rf`, sensitive file access)
- Exit code 2 blocking in PreToolUse hook prevents tool execution
- Multiple security layers with both prompt-level and tool-level filtering

### TTS Integration
- Intelligent text-to-speech with provider priority: ElevenLabs > OpenAI > pyttsx3
- AI-generated completion messages using LLM priority: OpenAI > Anthropic > Ollama
- Notification announcements for user input requests and sub-agent completion

### UV Single-File Scripts
All hooks use UV's single-file script format with embedded dependency declarations:
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///
```

This approach provides:
- Dependency isolation from main project
- Fast execution without virtual environment management
- Self-contained, portable scripts
- Automatic dependency resolution by UV

### Environment Variables
Optional environment variables for enhanced functionality:
- `OPENAI_API_KEY` - OpenAI API access for TTS and LLM services
- `ANTHROPIC_API_KEY` - Anthropic API for LLM completion messages
- `ELEVENLABS_API_KEY` - ElevenLabs TTS (premium audio quality)
- `ENGINEER_NAME` - Personalized audio messages and context

## Hook Flow Control

### Exit Code Behavior
- **Exit Code 0**: Success (stdout shown in transcript mode)
- **Exit Code 2**: Critical blocking error (stderr fed back to Claude automatically)
- **Other codes**: Non-blocking errors (stderr shown to user)

### JSON Output Control
Hooks can return structured JSON for sophisticated control:
```json
{
  "continue": true,
  "decision": "block",
  "reason": "Explanation for decision",
  "suppressOutput": true
}
```

### Blocking Capabilities
- **UserPromptSubmit**: Can block prompts, add context
- **PreToolUse**: Can block tool execution
- **Stop/SubagentStop**: Can prevent completion (use cautiously)
- **Other hooks**: Cannot block, provide feedback only

## Common Development Patterns

### Creating New Sub-Agents
Use the meta-agent to generate new specialized agents:
```bash
# Claude Code will automatically delegate to meta-agent
"Create a new sub-agent that runs tests and fixes failures"
```

### Custom Status Lines
Switch between status line versions in `.claude/settings.json`:
- `status_line.py` - Basic git info
- `status_line_v2.py` - Smart prompts with color coding  
- `status_line_v3.py` - Agent sessions with history
- `status_line_v4.py` - Extended metadata support

### Output Style Usage
Activate custom response formatting:
```bash
/output-style genui          # Beautiful HTML with embedded styling
/output-style table-based    # Organized markdown tables
/output-style ultra-concise  # Minimal words, maximum speed
```

### Session Data Management
Agent sessions are automatically tracked with:
- Unique agent names generated by LLM services
- Prompt history (configurable retention)
- Custom metadata via `/update_status_line` command

This repository serves as a comprehensive reference for advanced Claude Code customization and automation.