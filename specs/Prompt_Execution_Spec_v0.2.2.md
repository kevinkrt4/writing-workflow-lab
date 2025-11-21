# Prompt Execution Spec v0.2.2

## 1. Purpose
Define rules for compiling module prompts using preprocess_prompt.py, TEMPLATE_v1.9d, and prompt_config.yaml.

## 2. Components
- preprocess_prompt.py v0.2.2
- prompt_config.yaml
- TEMPLATE_v1.9d.txt
- validate_compiled_prompt() logic

## 3. Flow
1. Load YAML defaults and module config.
2. Load TEMPLATE file.
3. Substitute placeholders:
   - [MODULE]
   - [AUTHOR]
   - [BASENAME]
   - [OUTPUT_PATH]
   - [OUTPUT_FILENAME]
   - [PROMPT_VERSION]
   - [SPEC_VERSION]
   - [SCRIPT_VERSION]
4. Insert module-specific EVALUATE_BODY.
5. Validate compiled output.
6. Write final prompt to disk.

## 4. Validation Requirements
- No leftover placeholders.
- No <<<EVALUATE_BODY>>> token.
- Required identity lines present.
- Narrative_Synopsis requires:
  - ## Narrative Synopsis
  - ## Emotional and Philosophical Flow

## 5. Output Behavior
- Final compiled prompt asks user to upload one file.
- Output must be Markdown.
- Run metadata included at top.

## 6. Versioning
- prompt_version: v1.9d
- spec_version: 0.2.2
- script_version: 0.2.2
