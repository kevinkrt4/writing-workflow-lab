#!/usr/bin/env python3
"""
preprocess_prompt.py v0.2.2

Compile a module prompt from:
- prompt_config.yaml
- prompts/compiler_TEMPLATE_v1.9d.txt
- an input file (for basename only)

This script can be used:
- as a CLI tool (see main())
- or as a library (import build_prompt and load_config).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict

import yaml


class PromptError(Exception):
    """Base class for prompt-related errors."""


class PromptConfigError(PromptError):
    """Raised when the YAML config, template, or module selection is invalid."""


class PromptValidationError(PromptError):
    """Raised when the compiled prompt fails spec/validation checks."""


PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "prompt_config.yaml"
TEMPLATE_PATH = PROJECT_ROOT / "prompts" / "compiler_TEMPLATE_v1.9d.txt"


def determine_output_filename(
    basename: str,
    module_name: str,
    module_cfg: Dict[str, Any],
) -> str:
    """
    Determine the recommended output filename for this run.

    Prefer an explicit 'output_suffix' in the module config.
    Fall back to <basename>_<module_name>.md if none is provided.
    """
    suffix = module_cfg.get("output_suffix")
    if suffix:
        return f"{basename}_{suffix}.md"
    return f"{basename}_{module_name}.md"


# ============================================================
# Public API
# ============================================================


def build_prompt(
    input_file: Path,
    module_name: str,
    config: Dict[str, Any],
    override_output_path: str | None = None,
) -> str:
    """
    Build the compiled prompt for the given input file and module.

    Inputs:
    - input_file: full path to the input text file. The caller is responsible for
      validating that the file exists.
    - module_name: name of the module to use (must exist in config["modules"]).
    - config: loaded YAML configuration.
    - override_output_path: optional string path to override the metadata output path.

    Behavior:
    - Uses only the basename of the file when generating metadata and output filenames.
    - Module behavior and EVALUATE body are loaded from config["modules"][module_name].
    - Returns the compiled prompt text as a single string.

    Raises:
    - PromptConfigError: if the module is missing in config["modules"], the
      evaluate_body is empty, or required defaults are missing.
    - PromptValidationError: if the compiled prompt fails spec checks
      (unresolved placeholders, missing fragments/headings, etc.).
    """

    defaults = config.get("defaults", {})
    modules = config.get("modules", {})

    if module_name not in modules:
        raise PromptConfigError(f"Module '{module_name}' not found in config.modules")

    module_cfg = modules[module_name]

    author = defaults.get("author", "Unknown")

    if override_output_path:
        output_path = Path(override_output_path).expanduser().resolve().as_posix()
    else:
        output_path = defaults.get("output_path", str(PROJECT_ROOT))

    prompt_version = defaults.get("prompt_version", "v0.0.0")
    spec_version = defaults.get("spec_version", "0.0.0")
    script_version = defaults.get("script_version", "0.0.0")

    evaluate_body = module_cfg.get("evaluate_body", "").rstrip()
    if not evaluate_body:
        raise PromptConfigError(
            f"modules.{module_name}.evaluate_body is empty in config"
        )

    basename = input_file.stem
    output_filename = determine_output_filename(basename, module_name, module_cfg)

    template_text = load_template()

    substitutions = {
        "[MODULE]": module_name,
        "[AUTHOR]": author,
        "[BASENAME]": basename,
        "[OUTPUT_PATH]": output_path,
        "[OUTPUT_FILENAME]": output_filename,
        "[PROMPT_VERSION]": prompt_version,
        "[SPEC_VERSION]": spec_version,
        "[SCRIPT_VERSION]": script_version,
    }

    for placeholder, value in substitutions.items():
        template_text = template_text.replace(placeholder, value)

    # Insert module-specific EVALUATE body
    template_text = template_text.replace("<<<EVALUATE_BODY>>>", evaluate_body)

    validate_compiled_prompt(
        template_text, module_name, basename, output_filename, output_path
    )

    return template_text


# ============================================================
# Mid-level Helper Functions
# ============================================================


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Any]:
    """
    Load YAML config from the given path (default: CONFIG_PATH).

    Returns:
    - A dict with at least two top-level keys: "defaults" and "modules".

    Raises:
    - PromptConfigError: if the config file is missing or does not contain the
      required top-level keys.
    """
    if not path.is_file():
        raise PromptConfigError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if "defaults" not in data or "modules" not in data:
        raise PromptConfigError(
            "Config missing required top-level keys: defaults, modules"
        )

    return data


def validate_compiled_prompt(
    text: str,
    module_name: str,
    basename: str,
    output_filename: str,
    output_path: str,
) -> None:
    """
    Spec check for v0.2.2.

    Validates that the compiled prompt text conforms to the current spec:

    - No unresolved placeholders.
    - No leftover EVALUATE_BODY marker.
    - Run metadata block present.
    - Required identity lines present.
    - Required section headings for certain modules (e.g. Narrative_Synopsis).

    Raises:
    - PromptValidationError: if any of the above checks fail.
    """
    unresolved_tokens = [
        "[MODULE]",
        "[AUTHOR]",
        "[BASENAME]",
        "[OUTPUT_PATH]",
        "[OUTPUT_FILENAME]",
        "[PROMPT_VERSION]",
        "[SPEC_VERSION]",
        "[SCRIPT_VERSION]",
        "<<<EVALUATE_BODY>>>",
    ]

    leftovers = [tok for tok in unresolved_tokens if tok in text]
    if leftovers:
        raise PromptValidationError(
            "SpecViolation: unresolved placeholders in compiled prompt: "
            + ", ".join(leftovers)
        )

    must_contain = [
        f"Module: {module_name}",
        f"Input basename: {basename}",
        f"Recommended output filename: {output_filename}",
        f"Recommended output path: {output_path}",
        "Run metadata:",
        f"- Module: {module_name}",
        f"- Input basename: {basename}",
        f"- Recommended output filename: {output_filename}",
        f"- Recommended output path: {output_path}",
    ]

    missing = [frag for frag in must_contain if frag not in text]
    if missing:
        raise PromptValidationError(
            "SpecViolation: compiled prompt missing required fragments:\n"
            + "\n".join(f"- {m}" for m in missing)
        )

    if module_name == "Narrative_Synopsis":
        required_headings = [
            "## Narrative Synopsis",
            "## Emotional and Philosophical Flow",
        ]
        missing_headings = [h for h in required_headings if h not in text]
        if missing_headings:
            raise PromptValidationError(
                "SpecViolation: compiled prompt missing required section headings:\n"
                + "\n".join(f"- {h}" for h in missing_headings)
            )


def parse_args() -> argparse.Namespace:
    epilog = (
        "Example:\n"
        "  # 1) Compile the prompt file:\n"
        "  python3 preprocess_prompt.py \\\n"
        "      --input-file drafts/StarbucksNotebook1.txt \\\n"
        "      --module Narrative_Synopsis \\\n"
        "      -o StarbucksNotebook1_compiled_prompt.txt\n\n"
        "  # 2) Paste StarbucksNotebook1_compiled_prompt.txt into ChatGPT\n"
        "  #    ChatGPT then generates the final output file, e.g.:\n"
        "  #    StarbucksNotebook1_Narrative_Synopsis.md\n"
    )
    parser = argparse.ArgumentParser(
        prog="preprocess_prompt.py",
        description=(
            "Compile a module PROMPT file from prompt_config.yaml and the shared "
            "template (v0.2.2). The output is a compiled prompt you paste into ChatGPT, "
            "which then produces the final module output file."
        ),
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input-file",
        required=True,
        help=(
            "Required. Full path to the input text file. "
            "The basename (filename without extension) is used to generate output metadata."
        ),
    )
    parser.add_argument(
        "--module",
        required=True,
        help=(
            "Required. Module key to use from config.modules "
            "(e.g. Narrative_Synopsis)."
        ),
    )
    parser.add_argument(
        "-o",
        "--out",
        dest="output_file",
        help=(
            "Path to write the COMPILED PROMPT file (the file you paste into ChatGPT). "
            "Defaults to <basename>_compiled_prompt.txt in the current working directory. "
            "Note: This is NOT the final module output; it is the prompt that instructs "
            "ChatGPT to generate that output (for example, StarbucksNotebook1_Narrative_Synopsis.md)."
        ),
    )
    parser.add_argument(
        "--output-path",
        dest="override_output_path",
        help=(
            "Override the default output_path from YAML for METADATA ONLY. "
            "This controls the [OUTPUT_PATH] value inside the compiled prompt "
            "(i.e., the directory you want ChatGPT to suggest for the final module "
            "output file). It does NOT change where this script writes the compiled "
            "prompt itself; use -o/--out for that."
        ),
    )
    return parser.parse_args()


# ============================================================
# Internal Utility Functions
# ============================================================


def load_template() -> str:
    """
    Load the base prompt template.

    Returns:
    - The raw template text as a UTF-8 string.

    Raises:
    - PromptConfigError: if the template file cannot be found.
    """
    if not TEMPLATE_PATH.is_file():
        raise PromptConfigError(f"Template file not found: {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding="utf-8")


# ============================================================
# Entry Point
# ============================================================


def main() -> None:
    args = parse_args()

    # Load config and handle config-related errors
    try:
        config = load_config()
    except PromptConfigError as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)

    # Resolve input path directly from the CLI argument (no YAML path logic)
    input_path = Path(args.input_file).expanduser().resolve()

    if not input_path.is_file():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        raise SystemExit(1)

    try:
        compiled_prompt = build_prompt(
            input_file=input_path,
            module_name=args.module,
            config=config,
            override_output_path=args.override_output_path,
        )
    except PromptError as e:
        # Catches PromptConfigError and PromptValidationError
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)

    # Note:
    # - override_output_path (from --output-path) affects only the metadata
    #   inside the compiled prompt (recommended path for the final module output).
    # - output_file (from -o/--out) controls where THIS SCRIPT writes the compiled
    #   prompt file (the .txt you paste into ChatGPT).
    if args.output_file:
        out_path = Path(args.output_file).expanduser().resolve()
    else:
        out_path = Path.cwd() / f"{input_path.stem}_compiled_prompt.txt"

    out_path.write_text(compiled_prompt, encoding="utf-8")
    print(f"Wrote compiled prompt to: {out_path}")


if __name__ == "__main__":
    main()
