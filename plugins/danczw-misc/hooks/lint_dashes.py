#!/usr/bin/env python3
"""PostToolUse hook: flag em dashes the agent just wrote to a Markdown or text file.

Checks only the written text, not dashes already in the file. Reads both Claude Code
and Copilot CLI argument names. Claude Code gets the message via exit 2 and stderr,
Copilot CLI via additionalContext JSON on stdout.
"""
import json
import os
import sys

tool_input = json.load(sys.stdin).get("tool_input", {})
path = tool_input.get("file_path") or tool_input.get("path") or ""
edits = tool_input.get("edits") or [tool_input]
keys = ("content", "new_string", "file_text", "new_str")
text = "".join(e.get(k) or "" for e in edits for k in keys)
if path.endswith((".md", ".mdx", ".txt")) and "—" in text:
    msg = f"Em dash written to {path}: rewrite with a period, comma, colon or parentheses."
    if os.environ.get("COPILOT_PLUGIN_ROOT"):
        print(json.dumps({"additionalContext": msg}))
        sys.exit(0)
    print(msg, file=sys.stderr)
    sys.exit(2)
sys.exit(0)
