# Writing Workflow Compiler

This repository contains a Python-based compiler and Flask UI for building
structured prompts from local text drafts using YAML-configured modules.

The core pieces are:

- `preprocess_prompt.py` – compiles prompts using `prompt_config.yaml` and a template.
- `prompt_config.yaml` – defines available modules and their `evaluate_body` logic.
- `app.py` – Flask UI for selecting a module and draft file, compiling, and viewing the prompt.
- `drafts/` – input text files (`.txt` / `.md`) used as sources for compilation.
- `templates/` – Jinja2 templates for the Flask UI.

## Usage

### CLI compiler

From the repo root:

```bash
python3 preprocess_prompt.py \
  --input drafts/StarbucksNotebook1.txt \
  --module Narrative_Synopsis

