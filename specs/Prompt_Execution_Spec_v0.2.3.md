# Prompt Execution Spec v0.2.3

## 1. Purpose

Define the current Prompt Compiler contract for generating a Compiled Prompt
from:

- `tools/preprocess_prompt.py`
- `config/prompt_config.yaml`
- `prompts/compiler_TEMPLATE_v1.9d.txt`
- a selected Draft File path

This spec describes the behavior currently expected from `preprocess_prompt.py`
v0.2.3. It is a runtime contract for prompt compilation, not a full project
governance document.

## 2. Related Components

- `tools/preprocess_prompt.py`
- `config/prompt_config.yaml`
- `prompts/compiler_TEMPLATE_v1.9d.txt`
- `tests/test_preprocess_prompt.py`
- `tests/golden/sample_notebook_narrative_compiled_prompt.txt`

## 3. Scope

This spec applies to Prompt Compiler runs that use `preprocess_prompt.py`.

It defines:

- required input sources
- current template placeholders
- module lookup behavior
- output filename behavior
- runtime validation behavior
- CLI write behavior
- review/test-layer responsibilities

It does not define:

- provider/API execution
- local model execution
- browser UI behavior
- final model-generated writing output
- complete project-level architecture checks

## 4. Inputs

The Prompt Compiler uses:

- a Prompt Config YAML file containing top-level `defaults` and `modules` keys
- a Prompt Template at `prompts/compiler_TEMPLATE_v1.9d.txt`
- a selected input file path
- a module name matching a key in `config["modules"]`
- an optional metadata-only output path override
- an optional compiled-prompt output file path for the CLI

The current implementation uses only the input file stem for metadata and
recommended output filenames. It does not read the Draft File contents during
prompt compilation.

## 5. Prompt Config Contract

`load_config()` requires the config file to exist and contain these top-level
keys:

- `defaults`
- `modules`

The current default fields are:

- `author`
- `output_path`
- `prompt_version`
- `spec_version`
- `script_version`

If a default is missing, `build_prompt()` uses the current fallback values:

- author: `Unknown`
- output path: project root
- prompt version: `v0.0.0`
- spec version: `0.0.0`
- script version: `0.0.0`

## 6. Module Contract

The selected module must exist in `config["modules"]`.

Each selected module must provide a non-empty `evaluate_body`.

Each module may provide `output_suffix`. When present, the recommended final
module output filename is:

```text
<basename>_<output_suffix>.md
```

When `output_suffix` is missing, the fallback filename is:

```text
<basename>_<module_name>.md
```

## 7. Template Placeholder Contract

The current template uses square-bracket placeholders:

- `[MODULE]`
- `[AUTHOR]`
- `[BASENAME]`
- `[OUTPUT_PATH]`
- `[OUTPUT_FILENAME]`
- `[PROMPT_VERSION]`
- `[SPEC_VERSION]`
- `[SCRIPT_VERSION]`

The current module insertion marker is:

```text
<<<EVALUATE_BODY>>>
```

The Prompt Compiler replaces all listed placeholders and replaces
`<<<EVALUATE_BODY>>>` with the selected module's `evaluate_body`.

## 8. Compilation Order

Prompt compilation occurs in this order:

1. Load Prompt Config.
2. Resolve the selected module config.
3. Resolve required defaults and fallback values.
4. Resolve `evaluate_body`.
5. Determine the input basename.
6. Determine the recommended output filename.
7. Load the Prompt Template.
8. Replace square-bracket placeholders.
9. Replace `<<<EVALUATE_BODY>>>`.
10. Validate compiled prompt integrity.
11. Return the compiled prompt text.

The CLI writes the compiled prompt to disk only after `build_prompt()` returns
successfully.

## 9. Runtime Validation Boundary

Runtime validation in `preprocess_prompt.py` protects direct prompt compilation
correctness. It should catch errors that would produce an unusable Compiled
Prompt.

Runtime validation currently checks:

- config file exists
- config has required top-level keys
- selected module exists
- selected module `evaluate_body` is not empty
- template file exists
- compiled prompt has no unresolved known placeholders
- compiled prompt has no leftover `<<<EVALUATE_BODY>>>` marker
- compiled prompt contains required identity and run metadata fragments

Runtime validation is not responsible for full project governance.

## 10. Review/Test-Layer Boundary

Tests, golden tests, architecture checks, and future review checks protect
project integrity and drift.

Review/test-layer checks may enforce:

- active spec file exists
- template placeholder set matches this spec
- golden compiled prompt output remains stable
- config/script/spec versions remain coherent
- obsolete specs are archived or clearly marked
- template/spec/config changes are accompanied by tests or documented decisions
- provider imports remain behind provider adapter boundaries

These checks belong outside the runtime compiler unless they directly protect
the usability of one compiled prompt.

## 11. CLI Behavior

The CLI requires:

- `--input-file`
- `--module`

Optional CLI arguments:

- `-o` / `--out`: path for writing the Compiled Prompt file
- `--output-path`: metadata-only override for the recommended final module
  output path embedded inside the Compiled Prompt

If `-o` / `--out` is omitted, the CLI writes:

```text
<input_stem>_compiled_prompt.txt
```

in the current working directory.

CLI failures print an `Error:` message to standard error and exit with status
code `1`.

## 12. Output Contract

The compiler output is a Compiled Prompt intended for the GPT Web App upload
workflow.

The Compiled Prompt asks the model to request one uploaded input text file, then
run the selected module once on that uploaded file.

The Compiled Prompt includes:

- prompt/module identity
- author
- input basename
- recommended final module output filename
- recommended final module output path
- prompt/spec/script versions
- a run metadata block for the model to include in its final output
- module-specific EVALUATE instructions

The Compiled Prompt is not the final writing output.

## 13. Archived Specs

Older Prompt Execution Specs may be retained in `specs/archive/` for historical
context. Archived specs are not active contracts unless explicitly referenced by
current code, tests, or architecture checks.
