# Writing Workflow Lab

## Developer Environment Manual

### Version 1.0

---

# Table of Contents

1. **Maintenance Philosophy & Long-Term Strategy**
2. **Developer Setup Overview (Quickstart)**
3. **Backup, Archival, and Version Preservation**
4. **LLM Interaction Rules & Reset Protocols**
5. **Error Handling, Debugging & Recovery**
6. **Future Architecture & Refactor Plans**
7. **Packaging & Distribution**
8. **External Tool Integration**
9. **HTML Review Bundle Generator**
10. **GPT API Execution Layer**
11. **Chunking & Long-Form Processing Engine**

---

# 1. Maintenance Philosophy & Long-Term Strategy

## 1.1 Purpose of This System
The Writing Workflow Lab is both a creative and technical system. Over time, tools, models, and project needs will evolve. This manual exists to preserve stability, determinism, and clarity across that evolution.

## 1.2 Core Principles
- Maintain deterministic behavior across runs.
- Avoid drift between Template, Spec, compiler, and modules.
- Archive instead of deleting.
- Keep everything inspectable and plain text.
- Make updates intentional, documented, and minimal.

## 1.3 What "Long-Term Stability" Means
- Being able to return after months and immediately resume development.
- Ensuring new developer contributors can onboard without confusion.
- Guaranteeing compiled prompts behave consistently even if models evolve.

# 2. Developer Setup Overview (Quickstart)

## 2.1 System Requirements
- macOS (current dev environment)
- Python 3.14.x
- Git
- VS Code (with Python extension)

## 2.2 Clone the Repository
```
git clone <repo-url>
cd writing-workflow-lab
```

## 2.3 Create and Activate Virtual Environment
```
python3 -m venv ~/.venvs/prompts_env
source ~/.venvs/prompts_env/bin/activate
```

## 2.4 Recommended Shell Aliases
Add to `.zshrc` or `.bashrc`:
```
promptenv='source ~/.venvs/prompts_env/bin/activate'
promptui='code ~/GitHub/writing-workflow-lab'
```
Usage:
```
promptenv
promptui
```

## 2.5 Install Developer Tools
```
pip install black isort ruff python-dotenv
```

## 2.6 Select VS Code Interpreter
VS Code → Command Palette → Python: Select Interpreter → choose:
```
~/.venvs/prompts_env/bin/python
```

## 2.7 Test the Compiler
```
promptenv
python preprocess_prompt.py --module 001 --input drafts/StarbucksNotebook1.txt
```

## 2.8 VS Code Configuration
Your VS Code configuration for this project lives in:
```
.vscode/settings.json
```
It standardizes indentation, whitespace handling, and per-language formatting so the codebase stays consistent.

### 2.8.1 Global Editor Behavior
```jsonc
{
  "editor.detectIndentation": false,
  "editor.insertSpaces": true,
  "editor.tabSize": 2,
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true,
  "editor.renderWhitespace": "boundary",
  "[python]": {
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "[yaml]": {
    "editor.tabSize": 2,
    "editor.insertSpaces": true
  },
  "[markdown]": {
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "files.trimTrailingWhitespace": false
  },
  "[json]": {
    "editor.tabSize": 2,
    "editor.insertSpaces": true
  }
}
```

### 2.8.2 Python Formatting
- 4-space indentation
- Spaces only
- Black formatter is the default

### 2.8.3 YAML Formatting
- 2-space indentation
- Spaces only

### 2.8.4 Markdown Behavior
- 2-space indentation
- Trailing whitespace preserved (Markdown uses it for line breaks)

### 2.8.5 JSON Formatting
- 2-space indentation
- Spaces only

## 2.9 EditorConfig

The project includes a `.editorconfig` file that defines **universal, cross-editor formatting rules**. EditorConfig is supported by most modern editors (VS Code, Vim, JetBrains IDEs, Sublime Text, and others), ensuring consistent behavior regardless of which tool is used.

The `.editorconfig` file enforces foundational formatting rules:

- Character encoding  
- Line endings  
- Indentation type and size  
- Trimming trailing whitespace  
- Requiring a final newline  
- File-type-specific overrides

These settings form the baseline formatting contract that every tool follows.

### 2.9.1 How EditorConfig Differs from VS Code Settings

VS Code’s `settings.json` applies **only** within VS Code.  
`.editorconfig` applies **everywhere**.

| Concern | `.editorconfig` | `.vscode/settings.json` |
|--------|------------------|--------------------------|
| Scope | Any editor supporting EditorConfig | Only VS Code |
| Purpose | Enforce universal formatting rules | Control VS Code UI and behavior |
| Precedence in VS Code | Overrides VS Code formatting rules | Used only when no EditorConfig rule exists |
| Examples | Indentation, charset, line endings | Minimap, rulers, default formatter |

In practice:

- `.editorconfig` defines the **baseline** formatting rules.  
- `.vscode/settings.json` defines **VS Code–specific** workflow preferences (UI layout, whitespace rendering, preview theme, language-specific formatters).

Both layers work together to create a consistent and predictable editing environment.

### 2.9.2 Why We Include EditorConfig Even Though Everyone Uses VS Code

This project standardizes on **VS Code**, and `.vscode/settings.json` is the primary configuration for daily development.  
However, we include `.editorconfig` intentionally to “cover the bases.”

Reasons:

- **Cross-tool safety.** Current contributors use VS Code, but future contributors, CI tools, or GitHub-based editors may not. `.editorconfig` guarantees consistent formatting across all environments.
- **Formatting precedence.** VS Code automatically defers to `.editorconfig` for indentation, whitespace, and line-ending rules, ensuring those settings remain authoritative.
- **Portability.** CI pipelines, GitHub’s web editor, Codespaces, and external tools respect `.editorconfig` even when they ignore or bypass VS Code settings.

If you want to see the exact formatting rules, refer to the annotated copy in **Appendix A**.  
**Do not modify the `.editorconfig` file in the project directory.**  
It is maintained centrally, and changes affect formatting for the entire repository.

## 2.10 `.vimrc` Configuration

Vim uses a per-user configuration file named `.vimrc` to control editor behavior.
This file sits in the user’s home directory:

~/.vimrc

The `.vimrc` file defines core editor behavior such as syntax highlighting,
indentation, and navigation defaults. These settings apply globally unless
overridden by project-specific rules (e.g., `.editorconfig`).

### 2.10.1 Purpose

`.vimrc` provides a consistent editing baseline across all projects when using
Vim from the terminal (including remote SSH or lightweight edits outside VS
Code). This ensures predictable indentation and navigation even when not working
in the full IDE.

### 2.10.2 Location

Vim automatically loads configuration from:

~/.vimrc

No additional setup is required after the file is saved.

### 2.10.3 Configuration

Our standard `.vimrc` is intentionally minimal. It defines:

- an insert-mode shortcut,
- syntax highlighting and filetype detection,
- global indentation defaults,
- basic visual enhancements.

Current version:

" ,d inserts current date and time  
inoremap ,d <C-r>=strftime('%Y-%m-%d %H:%M') . ': '<CR>

" Syntax highlighting and editor basics  
syntax on  
filetype plugin indent on

" Indentation defaults (overridden by .editorconfig when present)  
set expandtab  
set tabstop=4  
set shiftwidth=4  
set softtabstop=4  
set autoindent  
set smartindent

" Editor UI settings  
set number  
set cursorline

### 2.10.4 Interaction with `.editorconfig`

Vim does not read `.editorconfig` natively. To enable support:

brew install editorconfig

Once installed, `.editorconfig` rules automatically take precedence over
`.vimrc` where applicable.

### 2.10.5 Recommended Usage

Use `.vimrc` for personal/global defaults.  
Use `.editorconfig` for project formatting rules.

This ensures:

- consistent indentation and formatting behavior across environments,
- shared project formatting rules are always honored,
- personal preferences never override project conventions.


# 3. Backup, Archival, and Version Preservation

## 3.1 What Must Be Preserved

There are three classes of artifacts:

1. **Tooling**: compiler, template, spec, validator, chunker, UI.
2. **Creative Inputs**: notebooks, manuscripts.
3. **Outputs**: module results, syntheses, HTML review bundles.

## 3.2 Archival Rules

- Never delete prior template or Spec versions.
- Move replaced versions to:
  - `prompts/archive/`
  - `specs/archive/`
  - `docs/archive/`
- Version everything.

## 3.3 Backups

- GitHub for tooling and documentation.
- Time Machine for entire repo + venv.
- Outputs stay outside Git (Downloads or project-specific directories).

---

# 4. LLM Interaction Rules & Reset Protocols

## 4.1 The Basis for Determinism

Every module run must behave like a pure function:

```
compiled_prompt + uploaded_file → deterministic_output
```

## 4.2 Interaction Rules

- Start each run with **reset**.
- Paste compiled prompt.
- The model asks for upload.
- Upload the file.
- Model must use **only** the uploaded file.
- No cross-session memory allowed.

## 4.3 Reset Rule

"reset" means:

- clear temporary context
- stop any active mode
- return to baseline
- do NOT erase saved long-term memory

---

# 5. Error Handling, Debugging & Recovery

## 5.1 Failure Layers

Errors typically fall into these layers:

- Spec
- Template
- Compiler
- Module
- Environment (Python, venv, VS Code)
- LLM behavior

## 5.2 Common Symptoms & Causes

- **Sections out of order** → Template drift
- **Missing placeholders** → Compiler mapping error
- **Model not asking for upload** → Broken Process Instructions
- **Compiler crash** → Python-level exception
- **Weird formatting** → Unicode or bad copy-paste

## 5.3 Recovery Process

1. Identify failing layer.
2. Fix only that layer.
3. Recompile.
4. Re-run module.
5. If environment broken → recreate venv.

---

# 6. Future Architecture & Refactor Plans

## 6.1 Likely Future Layout

```
src/writingwf/
    compiler/
    modules/
    validator/
    chunking/
    api/
    ui/
```

## 6.2 Refactor Principles

- Keep each subsystem isolated.
- Prefer new files over modifying complex ones.
- Preserve backward compatibility when possible.
- Document every structural change.

---

# 7. Packaging & Distribution

## 7.1 Purpose

Packaging allows:

- reproducible installs
- easy onboarding
- clean CLI tools
- shared runtime-only distributions

## 7.2 pyproject.toml (future)

Defines:

- dependencies
- version
- package metadata
- CLI entry points

## 7.3 Editable Development Install

```
pip install -e .
```

---

# 8. External Tool Integration

## 8.1 Markdown Review Tools

- Typora
- Obsidian

## 8.2 Development Tools

- VS Code
- Pandoc
- Static site generators (MkDocs, Astro, Jekyll, Hugo) optional

## 8.3 Purpose

Extend review workflows; keep core system simple.

---

# 9. HTML Review Bundle Generator

## 9.1 Purpose

Generate a portable, offline mini-site for multi-module outputs.

## 9.2 Output Structure

```
ReviewBundle/
    index.html
    modules/
        001.html
        002.html
    assets/css/theme.css
```

## 9.3 Use Cases

- Review of full manuscripts
- Editor collaboration
- Thumb-drive distribution

---

# 10. GPT API Execution Layer

## 10.1 Purpose

Automate module runs programmatically.

## 10.2 Key Components

- API client
- Runner
- Chain engine
- Logging

## 10.3 Capabilities

- Batch execution
- Long-form workflows
- Reproducible logs

---

# 11. Chunking & Long-Form Processing Engine

## 11.1 Purpose

Handle full-length manuscripts with deterministic chunking.

## 11.2 Method

- Split by paragraphs
- Add overlap
- Track metadata
- Run modules chunk-by-chunk

## 11.3 Merge Strategy

Hierarchical synthesis:

1. Chunk summaries
2. Section summaries
3. Full manuscript synthesis

## 11.4 Integration

- API runner
- HTML bundles
- Future validator

---

# End of Document

# Appendices

The appendices provide extended reference material and annotated examples that support the core sections of the Developer Environment Manual.

---

## Appendix Contents

- **Appendix A:** Annotated `.editorconfig`  
  A complete explanation of the project’s universal formatting rules, including an annotated copy of the `.editorconfig` file.

---

# Appendix A — Annotated `.editorconfig`

This appendix provides a fully annotated copy of the project’s `.editorconfig` file.  
The goal is to make the formatting rules transparent without requiring contributors to open or modify the actual file in the repository.

**Do not edit the `.editorconfig` file in the project directory.**  
It is centrally maintained, and changes affect formatting for the entire codebase.

The annotated version below exists solely for documentation and onboarding.

---

## A.1 Annotated `.editorconfig`

```ini
# Top-level EditorConfig file for the Writing Workflow Lab
# This file enforces universal formatting rules across all editors.

root = true

# ---------------------------------------------------------------------------
# Global defaults
# These rules apply to all files unless overridden by later sections.
# ---------------------------------------------------------------------------
[*]
charset = utf-8            # All files saved as UTF-8
end_of_line = lf           # Normalize line endings to LF
indent_style = space       # Always use spaces, never tabs
indent_size = 2            # Default indentation is 2 spaces
insert_final_newline = true # Ensure last line ends with newline
trim_trailing_whitespace = true # Strip trailing spaces on save

# ---------------------------------------------------------------------------
# Markdown-specific overrides
# Markdown linting tools often require trailing spaces for line breaks,
# so we disable trimming here.
# ---------------------------------------------------------------------------
[*.md]
trim_trailing_whitespace = false

# ---------------------------------------------------------------------------
# Python-specific overrides
# Python files follow the standard 4-space indentation.
# ---------------------------------------------------------------------------
[*.py]
indent_size = 4

# ---------------------------------------------------------------------------
# YAML files
# Consistent 2-space indentation across all YAML.
# ---------------------------------------------------------------------------
[*.yaml]
indent_size = 2
```

---

## A.2 When This File Matters

You will see `.editorconfig` rules take effect when:

- VS Code automatically corrects indentation or newline style  
- Git diffs show whitespace changes you didn’t manually make  
- A file is normalized when you save it  
- A GitHub Codespace or browser editor “magically” formats files correctly  

This is expected and ensures consistency for all contributors and tools.

---
