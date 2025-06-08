# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project that demonstrates Google ADK (Agent Development Kit) functionality with multi-agent systems. The project contains two main agent implementations:

1. **Court System** (`court/agent.py`) - A sophisticated judicial simulation with:
   - Prosecutor, Lawyer, and Judge agents using `LlmAgent`
   - `LoopAgent` for 3-round debates between prosecutor and lawyer
   - `SequentialAgent` to orchestrate the debate loop followed by judge's verdict

2. **Test Agent** (`test_agent/agent.py`) - A simple multi-agent coordinator with three sub-agents having different personalities (kind, mean, logical)

## Development Commands

This project uses `uv` for dependency management:

```bash
# Install dependencies
uv sync

# Run the main application
uv run python main.py

# Run a specific agent module
uv run python -m court.agent
uv run python -m test_agent.agent
```

## Architecture Notes

- Each agent module defines a `root_agent` variable that serves as the entry point
- Agents use environment variable `ADK_MODEL` to configure the LLM model (defaults differ between modules)
- The court system demonstrates complex agent orchestration patterns:
  - `LoopAgent` for iterative interactions
  - `SequentialAgent` for ordered execution
  - Nested agent hierarchies

## Dependencies

- **google-adk**: Core framework for building multi-agent systems
- Uses Python 3.13+ and uv for package management