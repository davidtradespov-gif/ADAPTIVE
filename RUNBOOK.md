# ADAPTIVE Runbook

## Persistence Contract

Every meaningful project change must be persisted in three places:

1. repository files in this project
2. linked Obsidian notes inside this project folder
3. Git history via commit and push

## Repo Memory Files

Read these first in every session:

- `AGENTS.md`
- `DATASETS.md`
- `MEMORY.md`
- `PROJECT_STATE.md`
- `RESEARCH_PRINCIPLES.md`
- `README.md`
- `RUNBOOK.md`

## Obsidian Mapping

Primary hub note:

- `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE\ADAPTIVE.md`

Supporting linked notes:

- `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE\Projects\ADAPTIVE\Project State.md`
- `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE\Projects\ADAPTIVE\Decisions.md`
- `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE\Projects\ADAPTIVE\Session Log.md`
- `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE\Projects\Projects Index.md`

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
