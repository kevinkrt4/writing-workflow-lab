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
## 8. Evaluate Block Requirements

The evaluate_body section of each module defines the runtime instructions that govern how ChatGPT analyzes the uploaded notebook.
This section establishes the mandatory structure, formatting rules, invariants, and allowed variations for all module Evaluate Blocks.

Evaluate Blocks are not free-form text.
They must conform to the following contract.

### 8.1 Purpose of the Evaluate Block

The Evaluate Block:

1. Describes how ChatGPT must analyze the uploaded notebook.
2. Provides module-specific rules for section structure and content.
3. Defines a fixed metadata template for the generated Markdown output.
4. Ensures consistent behavior across modules.

It is inserted directly into TEMPLATE_v1.9d at the <EVALUATE_BODY> placeholder.

### 8.2 Global Structure Requirements

All Evaluate Blocks must follow this global pattern:

1. Introductory line:
   You are running the <ModuleName> module.
2. Instruction to read the uploaded notebook:
   Read the uploaded notebook carefully.
   Build all analysis directly and exclusively from the text that is provided.
3. A section divider labeled OUTPUT REQUIREMENTS.
4. Ordered definitions of:
   - Metadata header rules
   - Output sections
   - Analysis behavior
   - Section-specific rules
   - Structural template
5. A closing instruction similar to:
   Output only the final Markdown document.
   No meta commentary. No process notes.

### 8.3 Required Metadata Header Rules

Every Evaluate Block must contain a section specifying that the generated YAML metadata header must include:

- title
- module
- source_file
- output_file
- date_generated
- summary

Mandatory constraints:

- YAML must not be wrapped in backticks or fences.
- All keys must be lowercase and spelled exactly as listed.
- summary must be 1-2 sentences.
- source_file must use:
  [basename].txt
- output_file must use the module canonical suffix:
  [basename]_<output_suffix>.md

These rules should be present, either explicitly or by clear paraphrase, in every module.

### 8.4 Required Global Wording

The following core ideas must appear in every Evaluate Block, using identical or very close wording:

- Read the uploaded notebook carefully.
- Build all analysis directly and exclusively from the text that is provided.
- Do not insert any meta commentary.
- Output only the final Markdown document.

Modules may add additional constraints but must not remove or weaken these statements.

### 8.5 Section Ordering Requirements

The module required output sections must be listed in the Evaluate Block in the exact order they are expected to appear in the generated Markdown output.

Examples:

- Character List -> Relationship Map -> Narrative Summary
- Theme Overview -> Detailed Theme Analyses -> Closing Summary
- Timeline Overview -> Detailed Beat Breakdown -> Scene Summary

The Evaluate Block is the authoritative source of required ordering.

### 8.6 Formatting and Content Restrictions

These formatting rules apply to all modules:

- Output must be ASCII-safe.
- No Unicode typographic quotes.
- No blockquotes in the generated output.
- No backticks in the metadata header.
- No creative embellishment that is not grounded in the text.
- No invented events, characters, or concepts.
- Inline excerpts are allowed; blockquote excerpts are forbidden.
- Headings must use Markdown H1/H2/H3 syntax with ASCII characters only.

### 8.7 Module-Specific Variations

A module may vary:

- Section titles
- Number of sections
- Section-specific analysis rules
- Bullet vs table vs paragraph format
- Metadata summary description
- The high-level analysis behavior relevant to that module

A module may not vary:

- Metadata header keys
- Output filename rules
- Introductory and closing instructions
- ASCII-only requirement

### 8.8 Forbidden Constructs

Evaluate Blocks must not contain:

- Backticks inside YAML
- Curly quotes
- HTML tags
- Code fences around the YAML header
- Blockquotes
- Unicode bullets
- Placeholder tokens other than those defined in Section 3
- Process commentary about being an AI

### 8.9 Compiler Interaction

The compiler treats the Evaluate Block as structured text and enforces:

- Placeholder substitution
- Evaluate Block insertion
- Validation that no <EVALUATE_BODY> token remains
- Validation that the metadata header uses [basename]_<output_suffix>.md

Future compiler versions may add deeper structural validation based on this section.
## 9. Evaluate Block Validation Rules (Compiler-Side)

The compiler may optionally validate Evaluate Blocks to ensure they conform to the
requirements defined in Section 8. These checks are non-destructive and do not
modify evaluate_body content; they only detect violations and provide warnings.

Future versions of preprocess_prompt.py (v0.3+) may implement these rules.

### 9.1 Validation Timing

Evaluate Block validation occurs after:

1. TEMPLATE_v1.9d has been loaded.
2. All placeholder substitutions have been applied.
3. The evaluate_body text has been inserted into the template.
4. The compiled prompt exists as a complete in-memory string.

Validation must never run on raw evaluate_body fragments.

### 9.2 Required Phrases

The compiler may check that the following phrases are present in the Evaluate Block:

- "Read the uploaded notebook carefully."
- "Build all analysis directly and exclusively from the text that is provided."
- "Do not insert any meta commentary."
- "Output only the final Markdown document."

These checks may be implemented as simple substring searches.

### 9.3 Metadata Header Requirements

The compiler may verify:

1. The metadata block contains the required keys:
   - title
   - module
   - source_file
   - output_file
   - date_generated
   - summary

2. The output_file field matches:
   [basename]_<output_suffix>.md

   where <output_suffix> is defined in the module config.

3. The metadata block is not wrapped in backticks or code fences.

4. The metadata block uses plain ASCII characters only.

### 9.4 Section Ordering

The compiler may check that the required output sections appear in the exact order
defined by the module’s evaluate_body.

Implementation note:

- The compiler must store an ordered list of required headings for each module.
- A simple regex-based scan may be used.

### 9.5 Forbidden Construct Checks

The compiler may check for:

- Blockquotes inside the metadata block or output sections.
- Backticks inside the YAML header.
- Curly quotes.
- HTML tags in analysis sections.
- Unicode bullets.
- Remaining placeholder tokens (e.g., [BASENAME], [MODULE], <EVALUATE_BODY>).

If detected, the compiler should emit a warning identifying:
- module name,
- line number (optional),
- a short description of the violation.

### 9.6 ASCII Enforcement

The compiler may verify that evaluate_body text uses standard ASCII.

Any non-ASCII characters should trigger a warning.

### 9.7 Non-Fatal Warnings

Evaluate Block validation is advisory.

Warnings must:
- Not abort compilation.
- Not modify the evaluate_body content.
- Not rewrite module definitions.

Warnings are metadata only and are intended to help maintain consistency across modules.

### 9.8 Future Expansion

Future versions of the validator may:

- Provide diffs highlighting structural drift between modules.
- Compare evaluate_body content against a schema.
- Enforce module-specific invariants beyond section ordering.
- Emit structured JSON warnings for CI or automated validation workflows.

## 10. Template Integration Rules (TEMPLATE_v1.9d Contract)

TEMPLATE_v1.9d is the master prompt template used by preprocess_prompt.py to
assemble the final compiled prompt. This section defines the required structure,
placeholders, and formatting rules that the template must follow.

These rules ensure stable integration between the template, the compiler, and
module evaluate_body definitions.

### 10.1 Template Purpose

TEMPLATE_v1.9d provides:

1. The overall structure of the compiled prompt.
2. All global instructions unrelated to module-specific analysis.
3. A consistent layout for user interaction:
   - metadata injection
   - module identification
   - file upload request
   - runtime notes
4. A precise insertion point for evaluate_body.

It must remain stable across all modules and all compiler versions in the 0.x.x
series unless explicitly versioned.

### 10.2 Required Placeholders

The template must expose the following placeholders, spelled exactly as shown:

- [MODULE]
- [AUTHOR]
- [BASENAME]
- [OUTPUT_PATH]
- [OUTPUT_FILENAME]
- [PROMPT_VERSION]
- [SPEC_VERSION]
- [SCRIPT_VERSION]

And the Evaluate Block placeholder:

- <EVALUATE_BODY>

These placeholders must appear exactly once unless otherwise documented.

### 10.3 Placeholder Substitution Rules

The compiler substitutes placeholders as follows:

- [MODULE] – module key name from prompt_config.yaml
- [AUTHOR] – defaults.author from YAML
- [BASENAME] – derived from input file name
- [OUTPUT_PATH] – defaults.output_path unless overridden by CLI
- [OUTPUT_FILENAME] – determined by determine_output_filename()
- [PROMPT_VERSION] – defaults.prompt_version
- [SPEC_VERSION] – defaults.spec_version
- [SCRIPT_VERSION] – defaults.script_version

Placeholders must never appear inside code fences or quotes.

### 10.4 Evaluate Block Insertion

The template must include exactly one instance of the literal token:

<EVALUATE_BODY>

The compiler replaces this token with the full evaluate_body text from the module
definition. The compiler must validate that no <EVALUATE_BODY> token remains after
insertion.

### 10.5 Metadata Injection Requirements

The template must contain a Metadata Section containing placeholders for:

- [MODULE]
- [AUTHOR]
- [BASENAME]
- [OUTPUT_FILENAME]
- [OUTPUT_PATH]
- [PROMPT_VERSION]
- [SPEC_VERSION]
- [SCRIPT_VERSION]

These metadata lines must be:

- top-aligned (appear at the top of the template)
- in plain ASCII
- not inside any code block
- one value per line

### 10.6 Required User Interaction Flow

The template must include:

1. A first instruction to prompt the user to upload a single notebook file.
2. A clear explanation that the model will read the file and apply the selected module.
3. Runtime markers identifying the module being executed.

This ensures consistent user experience across all modules.

### 10.7 Formatting Constraints

The template must follow these constraints:

- ASCII-only content.
- No code fences around evaluate_body.
- No blockquotes in the metadata area.
- No hidden or unused placeholders.
- No trailing whitespace after placeholder lines.
- Headings must use Markdown H1/H2/H3 syntax.

### 10.8 Template Stability Rules

TEMPLATE_v1.9d must not be modified without issuing a new version, for example:

- TEMPLATE_v1.9e
- TEMPLATE_v2.0
- TEMPLATE_v2.1

Changes requiring a new template version include:

- new placeholders
- removed placeholders
- changed insertion point for evaluate_body
- changed metadata structure
- changed output section structure

Minor whitespace or comment changes do not require a new version but must still
be committed and tracked.

### 10.9 Future Template Extensions

Future versions may:

- introduce optional blocks for warnings or diagnostics
- include conditional insertion logic
- expose additional placeholders for expanded metadata
- integrate with rich validation tools

All such changes must follow the versioning rules described in 10.8.
