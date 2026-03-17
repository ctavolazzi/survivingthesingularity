# AI Work Effort System

This file describes the work effort system used in this project.

## Directory Structure (Johnny Decimal)

Work efforts live in `work_efforts/` using a **Johnny Decimal** numbering scheme:

```
work_efforts/
├── devlog.md                           # Running project log
├── 00_project_management/              # Roadmaps, indices, meta
├── 10_development/                     # Features, bug fixes, refactors
├── 12_image_optimization_enhancements/ # Image pipeline work
├── 20_content/                         # Blog posts, book content, copy
├── 30_design_ui/                       # Visual design, UI changes
├── 40_infrastructure/                  # Hosting, CI, env config
├── 50_maintenance/                     # Deps, security, cleanup
├── 60_testing/                         # QA, test suites
├── 70_documentation/                   # Docs, guides, changelogs
├── 80_deployment/                      # Release, deploy tasks
└── 90_archive/                         # Completed / abandoned work
```

Files are named `<decimal-id>_<slug>.md` — e.g., `10_development/10.03_blog-refactor.md`.

> **Note:** This project does NOT use `active/`, `completed/`, or `archived/` subdirectories. Use the Johnny Decimal folders above.

## Work Effort Format

Each work effort is a markdown file with structured frontmatter and sections:

```markdown
---
title: "Title of the Work Effort"
status: "active" # options: active, paused, completed
priority: "medium" # options: low, medium, high, critical
assignee: "username"
created: "YYYY-MM-DD HH:MM" # Date and time
last_updated: "YYYY-MM-DD HH:MM" # Date and time
due_date: "YYYY-MM-DD" # Date only
tags: [tag1, tag2, tag3]
---

# Title of the Work Effort

## 🚩 Objectives
- Clear goal 1
- Clear goal 2

## 🛠 Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## 📝 Notes
- Context information
- Relevant details

## 🐞 Issues Encountered
- Obstacles or challenges

## ✅ Outcomes & Results
- Results achieved
- Lessons learned

## 📌 Linked Items
- [[Related File]]
- [[GitHub Issue #123]]

## 📅 Timeline & Progress
- **Started**: YYYY-MM-DD
- **Updated**: YYYY-MM-DD
- **Target Completion**: YYYY-MM-DD
```

## Work Effort Commands

Creating work efforts:
```
ai-setup work_effort --title "Feature Name" --priority high
ai-work-effort -i  # Interactive mode with more features
```

Listing work efforts:
```
ai-setup list
```

## Work Effort Locations

Work efforts are organized by domain using Johnny Decimal folders (see Directory Structure above). When a task is complete, move or note it in `work_efforts/90_archive/` or update its `status` field to `completed`.

Update `work_efforts/devlog.md` when closing significant work efforts.
