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

## Default Context

At the start of work in this repository, read and apply:

- `/Users/kevinthompson/GitHub/reference_library/chat_envs/core_compiled_env.md`
- `/Users/kevinthompson/GitHub/reference_library/chat_envs/project_compiled_env.md`

Treat these files as active operating context. Do not edit them directly because they are generated files.

## Git Rules

- Never commit without approval.
- Never push without approval.
