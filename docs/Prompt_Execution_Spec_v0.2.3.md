# Prompt Execution Spec v0.2.3

## 1. Purpose
Define rules for compiling module prompts using preprocess_prompt.py, TEMPLATE_v1.9d, and prompt_config.yaml.

## 2. Components
- preprocess_prompt.py v0.2.3  
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
- Final compiled prompt asks the user to upload one file.  
- Output must be Markdown.  
- Run metadata included at top.  

## 6. Versioning
- prompt_version: v1.9d  
- spec_version: 0.2.3  
- script_version: 0.2.3  

## 7. Module Output Filename Requirements

Each module defined in prompt_config.yaml must include an output_suffix field.  
This value is the single source of truth for constructing the module output filename.

### 7.1 Compiler Rule
The compiler determines the output filename using:

```
[basename]_[output_suffix].md
```

via:

```python
determine_output_filename()
```

### 7.2 Template Consistency Rule
Inside each module evaluate_body, the YAML metadata block must contain:

```
output_file: "[basename]_<output_suffix>.md"
```

The <output_suffix> must exactly match the module output_suffix field in prompt_config.yaml.

### 7.3 Module Addition Rule
When adding a new module:

1. Add an output_suffix field with the canonical suffix.  
2. Ensure the module evaluate_body YAML block uses the exact same suffix in the output_file line.  
3. No alternative spellings, hyphenations, additional spaces, or punctuation differences are allowed.  

### 7.4 Future Validation (recommended)
A future version of the compiler may validate that:

- The suffix parsed from the evaluate_body metadata block  
  matches the module output_suffix value.  

A mismatch should trigger a warning.
