# Prompt Execution Spec v0.2.3

## 1. Purpose
Define rules for compiling module prompts using preprocess_prompt.py, compiler_TEMPLATE_v1.9d, and prompt_config.yaml.

## 2. Related Components
- preprocess_prompt.py v0.2.3  
- prompt_config.yaml  
- compiler_TEMPLATE_v1.9d.txt  
- validate_compiled_prompt() logic  

## 3. Scope
This spec applies to all prompt generation modules executed using preprocess_prompt.py. It defines:

- Required metadata fields  
- Template structure  
- Placeholder substitution rules  
- Module-specific EVALUATE block insertion  
- Output validation constraints  

The behavior defined here is invariant across modules.

---

## 4. High-Level Overview

Prompt compilation consists of:

1. Loading compiler_TEMPLATE_v1.9d  
2. Injecting top-level metadata  
3. Substituting template placeholders  
4. Inserting module-specific EVALUATE_BODY code  
5. Writing the compiled output  
6. Validating the generated prompt  

These steps must occur in this exact order.

---

## 5. Definitions

**Template**  
compiler_TEMPLATE_v1.9d — a master text file containing:

- Static structure  
- Placeholders  
- Required metadata sections  
- A single `<EVALUATE_BODY>` token  

**Module**  
A configuration entry inside prompt_config.yaml containing:

- `output_suffix`  
- `description`  
- `evaluate_body` text  
- Other fields  

**Placeholder**  
A token enclosed in angle brackets, e.g., `<MODULE_NAME>`. They may appear once or multiple times.

---

## 6. Required Metadata Insertions

The compiler must populate:

- `<MODULE_NAME>`  
- `<BASENAME>`  
- `<AUTHOR>`  
- `<DATE>`  
- `<DATE_GENERATED>`  
- `<SOURCE_FILE>`  
- `<OUTPUT_FILE>`  
- `<OUTPUT_PATH>`  

Metadata must be inserted before any template substitutions except `<EVALUATE_BODY>`.

---

## 7. Placeholder Substitution Rules

1. All placeholders must be resolved except `<EVALUATE_BODY>`  
2. Unused placeholders generate validation failure  
3. A placeholder must map to a deterministic value  
4. Order of substitution must be preserved  

---

## 8. EVALUATE_BODY Insertion

### 8.1 Requirements
Each module defines its own text block in prompt_config.yaml:

```yaml
evaluate_body: |
  You are running the X module...
```

### 8.2 Insertion location
EVALUATE_BODY is inserted into compiler_TEMPLATE_v1.9d at the `<EVALUATE_BODY>` placeholder.

### 8.3 Constraints
- One and only one `<EVALUATE_BODY>` must exist in the template  
- If missing → validation error  
- If duplicated → validation error  

---

## 9. Output File Rules

The compiler must produce:

- A text output that merges:
  - compiler_TEMPLATE_v1.9d  
  - runtime metadata  
  - module-specific EVALUATE_BODY  
- A filename determined by:
  - `basename`  
  - `output_suffix`  

If no `output_suffix` exists, the fallback pattern is:

```
<basename>_<module_name>.md
```

---

## 10. Template Integration Rules (compiler_TEMPLATE_v1.9d Contract)

compiler_TEMPLATE_v1.9d is the master prompt template used by preprocess_prompt.py to:

- Control module formatting  
- Enforce consistent flow  
- Guarantee reproducible outputs  
- Standardize metadata structure  

### 10.1 Template Structure
compiler_TEMPLATE_v1.9d provides:

- A top banner  
- A metadata block  
- PROCESS INSTRUCTIONS  
- An EVALUATE BODY placeholder  
- Section markers  

### 10.2 Template Modification Rules
compiler_TEMPLATE_v1.9d must not be modified without issuing a new version, for example:

- compiler_TEMPLATE_v1.9e  
- compiler_TEMPLATE_v1.9f  

### 10.3 Placeholder Requirements
compiler_TEMPLATE_v1.9d must contain exactly:

- `<MODULE_NAME>`  
- `<BASENAME>`  
- `<SOURCE_FILE>`  
- `<OUTPUT_FILE>`  
- `<OUTPUT_PATH>`  
- `<AUTHOR>`  
- `<DATE>`  
- `<DATE_GENERATED>`  
- `<SUMMARY>`  
- `<EVALUATE_BODY>`  

### 10.4 Evaluate Block Insertion
It is inserted directly into compiler_TEMPLATE_v1.9d at the `<EVALUATE_BODY>` placeholder.

---

## 11. Validation Phase

Validation ensures:

1. compiler_TEMPLATE_v1.9d has been loaded  
2. Required metadata fields were populated  
3. All placeholders except `<EVALUATE_BODY>` were replaced  
4. The `<EVALUATE_BODY>` block exists exactly once  
5. Output format matches expected structure  
6. The output contains no unresolved placeholders  

---

## 12. Error Classes

### 12.1 Template Errors
Raised when:

- compiler_TEMPLATE_v1.9d cannot be read  
- compiler_TEMPLATE_v1.9d is missing required placeholders  
- compiler_TEMPLATE_v1.9d contains extra or duplicate placeholders  
- compiler_TEMPLATE_v1.9d does not contain exactly one `<EVALUATE_BODY>` token  

### 12.2 Metadata Errors
- Failure to populate required fields  
- Missing author  
- Missing source file  

### 12.3 Module Errors
- Invalid module name  
- Missing evaluate_body  
- Missing output_suffix (if required)  

---

## 13. Versioning

Each release of the Prompt Execution Spec corresponds to:

- A compiler version  
- A template version  
- A module registry version  

The version of compiler_TEMPLATE_v1.9d and its descendants must match the expected compiler version.

