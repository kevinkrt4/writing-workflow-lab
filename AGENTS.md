# AGENTS.md

## Default Behavior

Before making changes:

1. Analyze the problem.
2. Propose a plan.
3. Wait for approval.
4. Implement only after approval.
5. Show diffs before committing.

## Repository Principles

- Project files are the source of truth for Writers Workbench behavior.
- Shared context and reusable reference material should live in `reference_library`.
- Generated files should not be edited directly.
- Prefer manifest-driven workflows when a manifest exists.
- Human review is required before significant changes.

## Task Tracking

- Keep `/Users/kevinthompson/GitHub/reference_library/projects/writers_workbench/writers_workbench_backlog.md` current as the durable task-history record for Writers Workbench.
- Link active work and completed work to the relevant backlog item.
- Update the backlog when task status changes, especially before ending a work session.
- Treat memory files as session continuity only, not as the authoritative task record.

## Default Context

At the start of work in this repository, read and apply:

- `/Users/kevinthompson/GitHub/reference_library/chat_envs/core_compiled_env.md`
- `/Users/kevinthompson/GitHub/reference_library/chat_envs/project_compiled_env.md`
- `/Users/kevinthompson/GitHub/reference_library/projects/writers_workbench/writers_workbench_architecture_direction.md`
- `/Users/kevinthompson/GitHub/reference_library/projects/writers_workbench/writers_workbench_glossary.md`

Treat these files as active operating context. Do not edit them directly because they are generated files.

## Git Rules

- Never commit without approval.
- Never push without approval.
