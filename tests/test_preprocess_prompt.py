from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tools.preprocess_prompt import (
    PromptConfigError,
    build_prompt,
    determine_output_filename,
    load_config,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "prompt_config.yaml"
INPUT_FILE = PROJECT_ROOT / "drafts" / "StarbucksNotebook1.txt"


def test_determine_output_filename_prefers_configured_suffix() -> None:
    filename = determine_output_filename(
        "StarbucksNotebook1",
        "001-Narrative_Synopsis",
        {"output_suffix": "Narrative_Synopsis"},
    )

    assert filename == "StarbucksNotebook1_Narrative_Synopsis.md"


def test_build_prompt_compiles_narrative_prompt() -> None:
    config = load_config(CONFIG_PATH)

    prompt = build_prompt(
        input_file=INPUT_FILE,
        module_name="001-Narrative_Synopsis",
        config=config,
    )

    assert "# 001-Narrative_Synopsis Prompt (v1.9d)" in prompt
    assert "Module: 001-Narrative_Synopsis" in prompt
    assert "Input basename: StarbucksNotebook1" in prompt
    assert (
        "Recommended output filename: StarbucksNotebook1_Narrative_Synopsis.md"
        in prompt
    )
    assert "You are running the Narrative_Synopsis module." in prompt
    assert "<<<EVALUATE_BODY>>>" not in prompt


def test_build_prompt_rejects_unknown_module() -> None:
    config = load_config(CONFIG_PATH)

    with pytest.raises(PromptConfigError, match="Module 'missing' not found"):
        build_prompt(INPUT_FILE, "missing", config)


def test_cli_writes_compiled_prompt(tmp_path: Path) -> None:
    output_file = tmp_path / "compiled_prompt.txt"

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "tools" / "preprocess_prompt.py"),
            "--input-file",
            str(INPUT_FILE),
            "--module",
            "001-Narrative_Synopsis",
            "-o",
            str(output_file),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.startswith("Wrote compiled prompt to:")
    assert output_file.exists()
    assert "Narrative_Synopsis module" in output_file.read_text(encoding="utf-8")
