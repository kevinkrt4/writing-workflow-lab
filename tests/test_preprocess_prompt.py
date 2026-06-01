from __future__ import annotations

import re
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
ACTIVE_SPEC_PATH = PROJECT_ROOT / "specs" / "Prompt_Execution_Spec_v0.2.3.md"
TEMPLATE_PATH = PROJECT_ROOT / "prompts" / "compiler_TEMPLATE_v1.9d.txt"
SAMPLE_INPUT_FILE = PROJECT_ROOT / "tests" / "fixtures" / "sample_notebook.txt"
STARBUCKS_INPUT_FILE = PROJECT_ROOT / "drafts" / "StarbucksNotebook1.txt"
GOLDEN_PROMPT_FILE = (
    PROJECT_ROOT / "tests" / "golden" / "sample_notebook_narrative_compiled_prompt.txt"
)
EXPECTED_TEMPLATE_TOKENS = {
    "[MODULE]",
    "[AUTHOR]",
    "[BASENAME]",
    "[OUTPUT_PATH]",
    "[OUTPUT_FILENAME]",
    "[PROMPT_VERSION]",
    "[SPEC_VERSION]",
    "[SCRIPT_VERSION]",
    "<<<EVALUATE_BODY>>>",
}


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "tools" / "preprocess_prompt.py"),
            *args,
        ],
        check=False,
        capture_output=True,
        text=True,
    )


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
        input_file=STARBUCKS_INPUT_FILE,
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
        build_prompt(SAMPLE_INPUT_FILE, "missing", config)


def test_build_prompt_rejects_empty_evaluate_body() -> None:
    config = {
        "defaults": {},
        "modules": {
            "empty-module": {
                "evaluate_body": "",
            }
        },
    }

    with pytest.raises(
        PromptConfigError,
        match="modules.empty-module.evaluate_body is empty",
    ):
        build_prompt(SAMPLE_INPUT_FILE, "empty-module", config)


def test_build_prompt_matches_golden_narrative_prompt() -> None:
    config = load_config(CONFIG_PATH)

    prompt = build_prompt(
        input_file=SAMPLE_INPUT_FILE,
        module_name="001-Narrative_Synopsis",
        config=config,
    )

    expected = GOLDEN_PROMPT_FILE.read_text(encoding="utf-8")

    assert prompt == expected


def test_load_config_rejects_missing_config_file(tmp_path: Path) -> None:
    missing_config = tmp_path / "missing_prompt_config.yaml"

    with pytest.raises(PromptConfigError, match="Config file not found"):
        load_config(missing_config)


def test_load_config_rejects_missing_required_top_level_keys(tmp_path: Path) -> None:
    invalid_config = tmp_path / "prompt_config.yaml"
    invalid_config.write_text("defaults: {}\n", encoding="utf-8")

    with pytest.raises(
        PromptConfigError,
        match="Config missing required top-level keys: defaults, modules",
    ):
        load_config(invalid_config)


def test_template_contains_expected_prompt_compiler_tokens() -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    for token in EXPECTED_TEMPLATE_TOKENS:
        assert token in template


def test_active_spec_documents_current_prompt_compiler_tokens() -> None:
    spec = ACTIVE_SPEC_PATH.read_text(encoding="utf-8")

    for token in EXPECTED_TEMPLATE_TOKENS:
        assert token in spec

    assert "<MODULE_NAME>" not in spec
    assert re.search(r"(?<!<)<EVALUATE_BODY>(?!>)", spec) is None


def test_cli_writes_compiled_prompt(tmp_path: Path) -> None:
    output_file = tmp_path / "compiled_prompt.txt"

    result = run_cli(
        "--input-file",
        str(SAMPLE_INPUT_FILE),
        "--module",
        "001-Narrative_Synopsis",
        "-o",
        str(output_file),
    )

    assert result.returncode == 0
    assert result.stdout.startswith("Wrote compiled prompt to:")
    assert output_file.exists()
    assert "Narrative_Synopsis module" in output_file.read_text(encoding="utf-8")


def test_cli_rejects_missing_input_file(tmp_path: Path) -> None:
    missing_input = tmp_path / "missing_notebook.txt"
    output_file = tmp_path / "compiled_prompt.txt"

    result = run_cli(
        "--input-file",
        str(missing_input),
        "--module",
        "001-Narrative_Synopsis",
        "-o",
        str(output_file),
    )

    assert result.returncode == 1
    assert "Error: input file not found:" in result.stderr
    assert str(missing_input) in result.stderr
    assert not output_file.exists()


def test_cli_rejects_unknown_module(tmp_path: Path) -> None:
    output_file = tmp_path / "compiled_prompt.txt"

    result = run_cli(
        "--input-file",
        str(SAMPLE_INPUT_FILE),
        "--module",
        "missing",
        "-o",
        str(output_file),
    )

    assert result.returncode == 1
    assert "Error: Module 'missing' not found in config.modules" in result.stderr
    assert not output_file.exists()
