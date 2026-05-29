# Writers Workbench Developer Manual

## Purpose

This manual documents project-local setup, workflows, and operating procedures for Writers Workbench.

Global collaboration rules, voice guidance, glossary terms, and shared design principles live in `reference_library` and should not be duplicated here.

## Project Summary

Writers Workbench is a local-first human/AI collaborative environment for writing workflows, prompt orchestration, reusable analysis systems, and durable project context.

The project originated as a deterministic prompt-compilation system and is evolving toward a broader local workbench for resource selection, workflow execution, output review, and artifact management.

## Reference Context

Shared context is maintained in:

```text
~/GitHub/reference_library
```

Relevant source-of-truth files:

```text
~/GitHub/reference_library/canonical/core/core_chat_env.md
~/GitHub/reference_library/canonical/core/eng_voice_env.md
~/GitHub/reference_library/canonical/core/write_voice_env.md
~/GitHub/reference_library/canonical/core/ubiquitous_language_glossary.md
~/GitHub/reference_library/canonical/references/internal/design_principles.md
```

Use those files for:

- response block conventions
- engineering voice
- writing voice
- ubiquitous language
- local-first design principles
- human-reviewed workflow principles

This repo should only document how those concepts apply to Writers Workbench.

## Workbench Framing

The Flask application is the project interaction surface.

It should help the operator:

- select resources
- load context
- invoke workflows
- review outputs
- inspect system state
- approve actions

The workbench exposes capabilities clearly. It should not become the filesystem owner or an autonomous agent.

## System Requirements

Current development environment:

- macOS
- Python 3.11 or newer
- Git
- VS Code with Python extension

## Clone The Repository

```bash
git clone <repo-url>
cd writers_workbench
```

## Create And Activate A Virtual Environment

```bash
python3 -m venv ~/.venvs/prompts_env
source ~/.venvs/prompts_env/bin/activate
```

Recommended shell aliases:

```bash
alias promptenv='source ~/.venvs/prompts_env/bin/activate'
alias promptui='code ~/GitHub/writers_workbench'
```

## Install Developer Tools

```bash
pip install black isort ruff python-dotenv
```

If the project later adds package dependencies to `pyproject.toml`, prefer the documented project install command over one-off package installs.

## Start The Workbench

Use the launcher:

```bash
~/GitHub/writers_workbench/bin/start_workbench.sh start
```

Common launcher commands:

```bash
~/GitHub/writers_workbench/bin/start_workbench.sh start
~/GitHub/writers_workbench/bin/start_workbench.sh stop
~/GitHub/writers_workbench/bin/start_workbench.sh status
```

The local app runs at:

```text
http://127.0.0.1:5050
```

## Run The Prompt Compiler Directly

```bash
python tools/preprocess_prompt.py \
  --input-file drafts/StarbucksNotebook1.txt \
  --module Narrative_Synopsis
```

Show compiler help:

```bash
python tools/preprocess_prompt.py --help
```

Known arguments:

```text
--input-file
--module
--output-file
--author
```

## Editor Configuration

Project editor behavior is defined by:

```text
.editorconfig
.vscode/settings.json
```

`.editorconfig` provides cross-editor formatting defaults. `.vscode/settings.json` provides VS Code-specific workflow preferences.

Baseline expectations:

- UTF-8 files
- LF line endings
- final newline
- spaces instead of tabs
- Python formatted with Black-compatible settings
- Markdown trailing whitespace handled intentionally

Do not duplicate full editor configuration inside this manual. Open the actual config files when exact settings matter.

## Backup And Version Preservation

Preserve three classes of material:

1. Tooling: compiler, templates, specs, UI, workflow scripts.
2. Creative inputs: notebooks, manuscripts, drafts.
3. Outputs: module results, syntheses, HTML review bundles.

General rules:

- Use GitHub for tooling and documentation.
- Use local backups for the full repo and virtual environment.
- Keep large/generated outputs out of Git unless there is an explicit reason to version them.
- Preserve prior prompt and spec versions when they are still useful for comparison or rollback.

## Git Discipline

Before committing:

```bash
git status
git diff
git diff --cached
```

Preferred commit behavior:

- one conceptual change per commit when practical
- related files grouped intentionally
- avoid mixed commits unless unavoidable
- preserve working behavior during refactors
- write commit messages that explain operational intent

## Legacy Prompt Compilation Protocol

The original prompt-compilation workflow treated each module run as a controlled input/output operation:

```text
compiled_prompt + uploaded_file -> deterministic_output
```

That protocol still applies to legacy prompt modules and structured module execution.

Legacy interaction pattern:

1. Reset the model context.
2. Paste the compiled prompt.
3. Upload the selected source file.
4. Require the model to use only the uploaded source file.
5. Capture the output as a durable artifact.

The broader workbench direction allows controlled persistent project context, but that should be explicit and inspectable.

## Debugging And Recovery

Common failure layers:

- Spec
- Template
- Compiler
- Module
- Environment
- Model behavior

Common symptoms:

- Sections out of order: template or spec drift.
- Missing placeholders: compiler mapping problem.
- Compiler crash: Python exception or environment issue.
- Unexpected formatting: Markdown, Unicode, or copy/paste issue.
- Unexpected model behavior: prompt or context boundary problem.

Recovery process:

1. Identify the failing layer.
2. Fix only that layer.
3. Re-run the smallest relevant command.
4. Compare output before broadening the change.
5. Recreate the virtual environment only when the environment itself is broken.

## Architecture Direction

Likely future package layout:

```text
src/writers_workbench/
    interaction/
    orchestration/
    services/
    workflows/
    prompts/
    persistence/
    resources/
    ui/
```

Refactor principles:

- Keep each subsystem isolated.
- Prefer small migrations over broad rewrites.
- Preserve current workflows while improving structure.
- Document structural changes in project-local docs.
- Defer global terminology and principles to `reference_library`.

## Packaging Direction

Future packaging should support:

- reproducible installs
- clean CLI tools
- easier onboarding
- runtime-only usage where practical

Future editable install:

```bash
pip install -e .
```

## External Tool Integration

Useful external tools may include:

- VS Code
- Typora
- Obsidian
- Pandoc
- static site generators for exported review sites

External tools should extend review workflows without making the core system opaque.

## HTML Review Bundle Generator

Purpose: generate a portable offline review site for multi-module outputs.

Possible output shape:

```text
ReviewBundle/
    index.html
    modules/
        001.html
        002.html
    assets/css/theme.css
```

Use cases:

- manuscript review
- editor collaboration
- portable review packages
- publication-readiness passes

## API Execution Layer

Future API execution should support:

- batch module execution
- reproducible logs
- provider abstraction
- explicit run configuration
- inspectable output artifacts

Provider-specific code should remain behind adapters.

## Chunking And Long-Form Processing

Future long-form processing may need:

- paragraph-aware chunking
- overlap windows
- metadata tracking
- chunk-level summaries
- section-level synthesis
- full manuscript synthesis

This should be added only when current workflows need it.
