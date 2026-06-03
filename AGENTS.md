# Agent Operating Notes

This repository uses durable project memory. At the start of each session, read:

- `MEMORY.md`
- `PROJECT_STATE.md`
- `README.md`
- this `AGENTS.md`

## Required workflow

1. Inspect repo memory before acting.
2. Make changes conservatively and in context.
3. Verify results when practical.
4. Update repo memory for every meaningful change.
5. Commit intended changes with a clear message.
6. Push to the configured remote when possible.

## Persistence rules

- Durable instructions, decisions, bugs, fixes, and next steps must not live only in chat.
- If Obsidian sync is part of the workflow, keep repo memory and vault notes aligned.
- If Git push or Obsidian sync cannot be completed, record the failure clearly in repo memory and the session handoff.
