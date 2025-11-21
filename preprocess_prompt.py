#!/usr/bin/env python3
"""
preprocess_prompt.py v0.2.2

Compile a module prompt from:
- prompt_config.yaml
- prompts/TEMPLATE_v1.9d.txt
- an input file (for basename only)

Phase 1: single-file, Narrative_Synopsis-only module.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "prompt_config.yaml"
TEMPLATE_PATH = PROJECT_ROOT / "prompts" / "TEMPLATE_v1.9d.txt"


def load_config() -> Dict[str, Any]:
    """Load YAML config from prompt_config.yaml."""
    if not CONFIG_PATH.is_file():
        raise SystemExit(f"Config file not found: {CONFIG_PATH}")
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    # minimal shape checks
    if "defaults" not in data or "modules" not in data:
        raise SystemExit("Config missing required top-level keys: defaults, modules")
    return data


def load_template() -> str:
    """Load the base prompt template."""
    if not TEMPLATE_PATH.is_file():
        raise SystemExit(f"Template file not found: {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def build_prompt(input_file: Path, config: Dict[str, Any]) -> str:
    """
    Build the compiled prompt for the given input file.

    Phase 1 assumptions:
    - Single module: config['defaults']['module'] (Narrative_Synopsis)
    - One input file; we only use its basename.
    """
    if not input_file.is_file():
        raise SystemExit(f"Input file not found: {input_file}")

    defaults = config.get("defaults", {})
    modules = config.get("modules", {})

    module_name = defaults.get("module")
    if not module_name:
        raise SystemExit("defaults.module is not set in prompt_config.yaml")

    if module_name not in modules:
        raise SystemExit(f"Module '{module_name}' not found in config.modules")

    module_cfg = modules[module_name]

    author = defaults.get("author", "Unknown")
    output_path = defaults.get("output_path", str(PROJECT_ROOT))
    prompt_version = defaults.get("prompt_version", "v0.0.0")
    spec_version = defaults.get("spec_version", "0.0.0")
    script_version = defaults.get("script_version", "0.0.0")

    evaluate_body = module_cfg.get("evaluate_body", "").rstrip()
    if not evaluate_body:
        raise SystemExit(f"modules.{module_name}.evaluate_body is empty in config")

    basename = input_file.stem
    output_filename = f"{basename}_{module_name}.md"

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

    validate_compiled_prompt(template_text, module_name, basename, output_filename, output_path)

    return template_text


def validate_compiled_prompt(
    text: str,
    module_name: str,
    basename: str,
    output_filename: str,
    output_path: str,
) -> None:
    """
    Spec check for v0.2.2.

    - No unresolved placeholders.
    - No leftover EVALUATE_BODY marker.
    - Run metadata block present.
    - Required identity lines present.
    - Required section headings for Narrative_Synopsis present.
    """
    # 1. No unresolved placeholders
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
        raise SystemExit(
            "SpecViolation: unresolved placeholders in compiled prompt: "
            + ", ".join(leftovers)
        )

    # 2. Required identity / metadata fragments
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
        raise SystemExit(
            "SpecViolation: compiled prompt missing required fragments:\n"
            + "\n".join(f"- {m}" for m in missing)
        )

    # 3. Module-specific structure checks (Narrative_Synopsis)
    if module_name == "Narrative_Synopsis":
        required_headings = [
            "## Narrative Synopsis",
            "## Emotional and Philosophical Flow",
        ]
        missing_headings = [h for h in required_headings if h not in text]
        if missing_headings:
            raise SystemExit(
                "SpecViolation: compiled prompt missing required section headings:\n"
                + "\n".join(f"- {h}" for h in missing_headings)
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compile a module prompt from template and YAML config (v0.2.2).",
    )
    parser.add_argument(
        "input_file",
        help="Path to the input text file (used only to derive the basename).",
    )
    parser.add_argument(
        "-o",
        "--out",
        dest="output_file",
        help=(
            "Path to write the compiled prompt. "
            "Defaults to <basename>_compiled_prompt.txt in the current working directory."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input_file).expanduser().resolve()
    config = load_config()

    compiled_prompt = build_prompt(input_path, config)

    if args.output_file:
        out_path = Path(args.output_file).expanduser().resolve()
    else:
        out_path = Path.cwd() / f"{input_path.stem}_compiled_prompt.txt"

    out_path.write_text(compiled_prompt, encoding="utf-8")
    print(f"Wrote compiled prompt to: {out_path}")


if __name__ == "__main__":
    main()
