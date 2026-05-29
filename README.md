# Writers Workbench

Writers Workbench is a local-first human/AI collaborative environment for writing workflows, prompt orchestration, reusable analysis systems, and durable project context.

Current components:
- a Flask-based interaction surface
- a prompt compiler
- YAML-configured workflow modules
- local draft processing
- reusable orchestration infrastructure

The project originated as a deterministic prompt-compilation system and is gradually evolving toward a broader local-first orchestration environment.

---

# Launcher

Syntax:

```text
~/GitHub/writers_workbench/bin/start_workbench.sh start
~/GitHub/writers_workbench/bin/start_workbench.sh stop
~/GitHub/writers_workbench/bin/start_workbench.sh status
```

---

# To Start the Workbench

Run:

```bash
~/GitHub/writers_workbench/bin/start_workbench.sh start
```

The launcher:
- activates the Python virtual environment
- starts the Flask server
- opens Writers Workbench in Safari
- supervises the Flask process lifecycle

If the launch succeeds you will see something like:

```text
Starting Writers Workbench...
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5050
```

Writers Workbench will open in Safari at:

```text
http://127.0.0.1:5050
```

---

# To Stop the Workbench

Run:

```bash
~/GitHub/writers_workbench/bin/start_workbench.sh stop
```

This terminates the Flask server cleanly.

---

# To Check Status

Run:

```bash
~/GitHub/writers_workbench/bin/start_workbench.sh status
```

Example:

```text
Writers Workbench is running at http://127.0.0.1:5050
```

---

# To Run the Prompt Compiler Directly

```bash
python tools/preprocess_prompt.py \
  --input-file drafts/StarbucksNotebook1.txt \
  --module Narrative_Synopsis
```

Show compiler help:

```bash
python tools/preprocess_prompt.py --help
```

Arguments:

```text
--input-file
--module
--output-file
--author
```

---

# Repository Layout

- `AGENTS.md`
  Local agent operating instructions for this repository.

- `app.py`
  Flask interaction surface.

- `tools/preprocess_prompt.py`
  Prompt compiler and orchestration layer.

- `config/prompt_config.yaml`
  Workflow/module definitions.

- `prompts/`
  Canonical prompt templates.

- `drafts/`
  Local source notebooks and manuscripts.

- `templates/`
  Flask/Jinja2 UI templates.

- `specs/`
  Execution specifications and workflow contracts.

Project documentation lives in `reference_library`:

```text
~/GitHub/reference_library/projects/writers_workbench/
```

---

# Architecture Direction

The system is evolving toward:
- reusable workflow orchestration
- persistent local context
- interaction surfaces
- modular services
- filesystem durability
- inspectable AI collaboration
- local-first operation

Shared AI collaboration context, design principles, and project reference docs are maintained in `reference_library`.
