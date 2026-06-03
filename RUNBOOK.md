# ADAPTIVE Runbook

## Persistence Contract

Every meaningful project change must be persisted in three places:

1. repository files in this project
2. linked Obsidian notes in the vault at `C:\Users\david\OneDrive - My Biologics Pty Ltd\Documents\Obsidian Vault`
3. Git history via commit and push

## Repo Memory Files

Read these first in every session:

- `AGENTS.md`
- `MEMORY.md`
- `PROJECT_STATE.md`
- `README.md`
- `RUNBOOK.md`

## Obsidian Mapping

Primary hub note:

- `C:\Users\david\OneDrive - My Biologics Pty Ltd\Documents\Obsidian Vault\ADAPTIVE.md`

Supporting linked notes:

- `C:\Users\david\OneDrive - My Biologics Pty Ltd\Documents\Obsidian Vault\Projects\ADAPTIVE\Project State.md`
- `C:\Users\david\OneDrive - My Biologics Pty Ltd\Documents\Obsidian Vault\Projects\ADAPTIVE\Decisions.md`
- `C:\Users\david\OneDrive - My Biologics Pty Ltd\Documents\Obsidian Vault\Projects\ADAPTIVE\Session Log.md`
- `C:\Users\david\OneDrive - My Biologics Pty Ltd\Documents\Obsidian Vault\Projects\Projects Index.md`

## Minimum Session Steps

1. Read repo memory files.
2. Read the Obsidian `ADAPTIVE` hub note and the latest session note if present.
3. Do the work.
4. Verify the result.
5. Update repo memory.
6. Update the Obsidian notes.
7. Run `git status`.
8. Stage only intended files.
9. Commit with a clear message.
10. Push to `origin main`.

## Failure Handling

- If Obsidian cannot be updated, record the missing sync in repo memory before ending the session.
- If `git push` fails, record the exact error in repo memory and Obsidian before ending the session.
- Do not silently skip persistence.
