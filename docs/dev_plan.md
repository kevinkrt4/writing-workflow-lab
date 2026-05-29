# Development Architecture Notes

## Purpose

This document tracks project-specific architecture direction for Writers Workbench.

Shared collaboration rules, response indexing, voice guidance, glossary terms, and broad design principles are owned by `reference_library`. This document should not duplicate those definitions.

## Reference Context

Use these files as the source of truth for global environment and design guidance:

```text
~/GitHub/reference_library/canonical/core/core_chat_env.md
~/GitHub/reference_library/canonical/core/eng_voice_env.md
~/GitHub/reference_library/canonical/core/write_voice_env.md
~/GitHub/reference_library/canonical/core/ubiquitous_language_glossary.md
~/GitHub/reference_library/canonical/references/internal/design_principles.md
```

Writers Workbench may implement features that use those concepts, but the concepts themselves should remain centralized in `reference_library`.

## Core Direction

Writers Workbench is evolving from a deterministic prompt runner into a local-first writing workbench.

The Flask application should become the project interaction surface where the operator can:

- select local resources
- load project context
- invoke writing workflows
- inspect output
- review system state
- approve file changes or publication steps

The system should remain:

- incremental
- filesystem-first
- workflow-centered
- artifact-oriented
- provider-replaceable
- human-reviewed

Avoid hidden automation, premature abstraction, and large rewrites that discard working behavior.

## Project Responsibilities

Writers Workbench owns project-local implementation concerns:

- writing workflow execution
- prompt compilation
- local resource selection
- output generation
- review bundle generation
- project persistence
- UI controls for workflow orchestration
- adapters that call external model providers

`reference_library` owns shared conceptual context:

- collaboration rules
- response block conventions
- voice environments
- glossary terms
- reusable reference material
- cross-project design principles

## Architecture Boundaries

Keep responsibilities separated:

```text
Interaction Surface
    Flask routes, templates, static assets

Workflow Layer
    module selection, prompt compilation, workflow execution

Resource Layer
    drafts, prompts, specs, outputs, references

Persistence Layer
    project state, run history, artifacts, indexes

Model Boundary
    provider adapters behind a stable local interface
```

Core application code should avoid direct dependency on a specific provider SDK. Provider-specific behavior should live behind adapters.

## Current Stack

Current lightweight stack:

```text
Flask
pathlib
PyYAML
Black
isort
ruff
```

Likely future additions should be justified by concrete workflow needs:

```text
sqlite3       persistent local run state
mistune       Markdown rendering
LiteLLM       provider abstraction
```

Use libraries for commodity mechanics. Keep project-specific workflow semantics in the application.

## Persistence Direction

The project should move toward durable local state for conversations, workflow runs, artifacts, and exports.

Possible future structure:

```text
chat_store/
    chats/
    artifacts/
    exports/
    indexes/
```

Possible per-chat structure:

```text
C0001/
    chat.jsonl
    blocks.jsonl
    artifacts/
    summaries/
```

This is a direction, not an immediate implementation requirement.

## Resource Model

The project should evolve from specialized notebook selection toward a general resource model.

Resources may include:

- draft files
- prompt templates
- specs
- workflow configs
- generated outputs
- review bundles
- reference-library files
- saved conversations
- summaries

General pattern:

```text
Resource selection
    -> Workflow action
        -> Durable artifact
```

## Agent And Tool Philosophy

Avoid heavy provider-specific agent frameworks in the core architecture.

The workbench should own orchestration semantics. Deterministic scripts should perform deterministic work. Model calls should be explicit, inspectable, and reviewable.

Possible future project-local agents or services:

- PromptCompilerAgent
- PublicationAgent
- ReviewBundleAgent
- HistoryMiningAgent

These should be project abstractions, not vendor-owned architecture.

## Immediate Scope

Current implementation goals:

1. Preserve the existing prompt compiler workflow.
2. Keep the Flask workbench usable.
3. Clean up project documentation.
4. Clarify ownership between Writers Workbench and `reference_library`.
5. Add model/provider abstraction only when the API execution path needs it.
6. Add persistence incrementally after current workflows are stable.

Avoid:

- multi-agent systems
- autonomous orchestration
- premature database complexity
- overbuilt memory systems
- broad rewrites without a working migration path

## Strategic Principle

The goal is not to build a generic chatbot.

The goal is to build a local writing workbench where conversation, files, prompts, workflows, and outputs can be handled as durable project materials.
