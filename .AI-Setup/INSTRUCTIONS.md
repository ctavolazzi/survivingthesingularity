# AI-Setup Instructions

This directory contains context documents that are automatically available to AI assistants (autoseeded) at the start of each session.

## Document Map

| File | Purpose |
|------|---------|
| `INSTRUCTIONS.md` | This file — quick orientation |
| `AI-work-effort-system.md` | Work effort format and Johnny Decimal folder structure |
| `AI-setup-instructions.md` | `ai-setup` pip tooling reference (optional, not required) |
| `AI-setup-validation-instructions.md` | Validation checklist for AI setup |

## Authoritative Project Context

The root `CLAUDE.md` is the **primary** project context file. Read it first. The files in this directory supplement it with tooling and convention details.

## Work Efforts

This project uses a **Johnny Decimal** system in `work_efforts/` — not generic `active/completed/archived` folders. See `AI-work-effort-system.md` for the full structure and file format.

## Optional Tooling (`ai-setup` pip package)

If the `ai-setup` package is installed (`pip3 install ai-setup`), these commands are available:

```bash
ai-setup work_effort --title "Feature Name" --priority high
ai-work-effort -i                          # interactive mode
ai-work-effort --use-ai --description "…"  # AI-generated content (requires Ollama)
ai-setup list                              # list work efforts
```

The tooling is optional. Work efforts can be created manually as markdown files.
