#!/usr/bin/env python3
"""
Script: preprocess_prompt.py
Description: Spec-aligned prompt renderer for the writing workflow.
Version: (see SCRIPT_VERSION below)

Purpose:
  - Contain the master prompt template text internally (TEMPLATE).
  - Read prompt_config.yaml for:
        module, author, output_path.
  - Substitute placeholders inside TEMPLATE.
  - Emit a fully rendered prompt either to:
        - an explicit -o/--output file, or
        - by default: [module]_Prompt.txt

This script is aligned with the Prompt Execution Spec (see SPEC_VERSION below):
  - Required sections in this order:
      YAML HEADER
      PROCESS INSTRUCTIONS (including Step 3.5 Metadata Template)
      NOTES
      EVALUATE BLOCK
  - EVALUATE explicitly instructs the assistant to:
      1) prepend the metadata block defined in Step 3.5, and
      2) then generate only the sections specified there.

Placeholders supported (header + body):
  [MODULE]          or {{ MODULE }}
  [AUTHOR]          or {{ AUTHOR }}
  [OUTPUT_PATH]     or {{ OUTPUT_PATH }}
  [PROMPT_VERSION]  or {{ PROMPT_VERSION }}
"""

from pathlib import Path
import argparse

try:
    import yaml
except ImportError:
    yaml = None

SCRIPT_NAME = Path(__file__).name
SCRIPT_VERSION = "0.2.1"

SPEC_NAME = "Prompt Execution Spec"
SPEC_VERSION = "0.2.1"
SPEC_LABEL = f"{SPEC_NAME} v{SPEC_VERSION}"

PROMPT_VERSION = "v1.9c"  # canonical version of the embedded template

DEFAULT_CONFIG_NAME = "prompt_config.yaml"


# --------------------------------------------------------------------
# MASTER TEMPLATE (spec-compliant, Narrative_Synopsis-flavored module)
# --------------------------------------------------------------------
TEMPLATE = """# [MODULE] Prompt ([PROMPT_VERSION])

---
title: "[basename] - [MODULE]"
author: "[AUTHOR]"
module: "[MODULE]"
source_file: "(filled automatically at runtime)"
output_file: "(filled automatically at runtime)"
output_path: "[OUTPUT_PATH]"
date: "(filled automatically at runtime)"
date_generated: "(filled automatically at runtime)"
feedback:
  mode: "inline"
  verbosity: "concise"
summary: >
  Generates a cohesive, emotionally resonant analysis of the uploaded text
  according to the logic defined in the [MODULE] prompt.
---

PROCESS INSTRUCTIONS

1. Prompt the user to upload exactly one .txt file.

2. Prompt once for author name (blank -> "unknown").
   This step MUST be executed every time the prompt is run.

3. Process the uploaded file and fill metadata at runtime:
   - title = "[basename] - [MODULE]"
   - author = (captured from prompt or defaults to "unknown")
   - source_file = "(absolute path of uploaded input file)"
   - output_file = "[basename]_[MODULE].md"
   - date = current local date at runtime
   - date_generated = full ISO timestamp at runtime.

All placeholders for these fields must be resolved at runtime before E-MODE output begins.

3.5. Prepend Metadata Block

---
title: "[basename] - [MODULE]"
author: "(captured author name)"
module: "[MODULE]"
source_file: "(absolute path of uploaded input file)"
output_file: "[basename]_[MODULE].md"
output_path: "[OUTPUT_PATH]"
date: "(current local date)"
date_generated: "(full ISO timestamp)"
feedback:
  mode: "inline"
  verbosity: "concise"
summary: >
  Generates a cohesive, emotionally resonant analysis of the uploaded text,
  following the logic defined by the [MODULE] prompt.
---

# Output File Naming Convention
# [basename]_[MODULE].md

NOTES

- Output format: Markdown with a YAML header.
- ASCII-only punctuation and headings (##, ###).
- The prepended metadata block must be the first content in the final output.

---
EVALUATE: |
  First, prepend the full YAML metadata block defined in Step 3.5 above,
  substituting runtime values for:
    - [basename]
    - [MODULE]
    - [OUTPUT_PATH]
    - captured author name
    - absolute path of uploaded input file
    - current local date
    - full ISO timestamp

  Then, after the metadata block, produce the following sections:

  1. Narrative Synopsis (2-5 paragraphs)
     Provide a cohesive, emotionally resonant narrative synopsis tracing
     the story's flow, tone, and emotional progression.

  2. Emotional and Philosophical Flow (1-2 paragraphs)
     Describe how the emotional and philosophical insights evolve through
     the text.
---
"""


# --------------------------------------------------------------------
def load_config(config_path: Path) -> dict:
    """Load YAML config (module, author, output_path)."""
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    if yaml is None:
        raise RuntimeError("PyYAML is required to load prompt_config.yaml (missing PyYAML).")

    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return data

def debug_print(msg: str, debug_enabled: bool):
    """Print a debug message only if --debug is enabled."""
    if debug_enabled:
        print(f"[{SCRIPT_NAME} v{SCRIPT_VERSION} DEBUG] {msg}", flush=True)

def validate_config(cfg: dict) -> None:
    """Ensure required keys are present and non-empty.

    Required keys:
      - module
      - author
      - output_path
    """
    required = ["module", "author", "output_path"]
    missing = [key for key in required if not cfg.get(key)]
    if missing:
        missing_str = ", ".join(missing)
        raise RuntimeError(
            f"prompt_config.yaml is missing required key(s): {missing_str}. "
            "All of these must be defined for a spec-compliant prompt."
        )

def apply_replacements(text: str, cfg: dict) -> str:
    """Perform placeholder substitution using values from cfg."""
    replacements = {
        "[MODULE]": cfg.get("module", ""),
        "{{ MODULE }}": cfg.get("module", ""),

        "[AUTHOR]": cfg.get("author", ""),
        "{{ AUTHOR }}": cfg.get("author", ""),

        "[OUTPUT_PATH]": cfg.get("output_path", ""),
        "{{ OUTPUT_PATH }}": cfg.get("output_path", ""),

        "[PROMPT_VERSION]": PROMPT_VERSION,
        "{{ PROMPT_VERSION }}": PROMPT_VERSION,
    }

    for token, value in replacements.items():
        text = text.replace(token, value)

    return text


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Render embedded prompt template (spec v0.2.1-aligned)."
    )
    parser.add_argument(
        "--module",
        help="Name of the module to run (narrative, outline, characters, synthesis).",
    )
    parser.add_argument(
        "--input",
        help="Path to the input text file.",
    )
    parser.add_argument(
        "-c",
        "--config",
        help=f"Path to config YAML (default: {DEFAULT_CONFIG_NAME} in current directory).",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file path. Defaults to [module]_Prompt.txt.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print script version and exit.",
    )
    args = parser.parse_args(argv)

    # Handle --version
    if args.version:
        print(f"{SCRIPT_NAME} v{SCRIPT_VERSION}", flush=True)
        print(f"[{SCRIPT_NAME}] Using {SPEC_LABEL}", flush=True)
        return 0

    # Version banner for normal runs
    print(f"[{SCRIPT_NAME} v{SCRIPT_VERSION}] Starting run", flush=True)
    print(f"[{SCRIPT_NAME}] Using {SPEC_LABEL}", flush=True)

    # Determine config path
    if args.config:
        config_path = Path(args.config)
    else:
        config_path = Path.cwd() / DEFAULT_CONFIG_NAME
    debug_print(f"config_path = {config_path}", args.debug)

    cfg = load_config(config_path)
    validate_config(cfg)

    # Render the template
    rendered = apply_replacements(TEMPLATE, cfg)

    # Determine output path
    module_name = cfg.get("module", "Prompt")
    default_output = Path.cwd() / f"{module_name}_Prompt.txt"

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = Path(default_output)
    debug_print(f"out_path = {out_path}", args.debug)

    out_path.write_text(rendered, encoding="utf-8")
    print(f"Rendered prompt written to: {out_path}")


if __name__ == "__main__":
    main()
