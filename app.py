from pathlib import Path

from flask import Flask, flash, render_template, request

from preprocess_prompt import (
    PromptConfigError,
    PromptError,
    PromptValidationError,
    build_prompt,
    load_config,
)

app = Flask(__name__)
app.secret_key = "change-me"

# --------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent  # writing-workflow-lab/
CONFIG_PATH = BASE_DIR / "prompt_config.yaml"
DRAFTS_DIR = BASE_DIR / "drafts"

# --------------------------------------------------------------------
# Load configuration once at startup
# --------------------------------------------------------------------

try:
    PROMPT_CONFIG = load_config(CONFIG_PATH)
except (PromptConfigError, PromptError) as e:
    # Fail early if the config is invalid
    raise RuntimeError(f"Failed to load prompt configuration: {e}")

# --------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------


def list_draft_files() -> list[str]:
    """Return .txt and .md files from drafts/."""
    if not DRAFTS_DIR.exists():
        return []

    files: list[Path] = []
    files.extend(DRAFTS_DIR.glob("*.txt"))
    files.extend(DRAFTS_DIR.glob("*.md"))

    # Return sorted file names (strings)
    return sorted([p.name for p in files], key=str)


def list_modules() -> list[str]:
    """Return a simple list of module keys from PROMPT_CONFIG."""
    modules = PROMPT_CONFIG.get("modules", {})
    return sorted(modules.keys())


# --------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------


@app.route("/", methods=["GET", "POST"])
def index():
    draft_files = list_draft_files()
    modules = list_modules()

    compiled_prompt = ""
    selected_file = None
    selected_module = None

    if request.method == "POST":
        selected_module = request.form.get("module")
        selected_file = request.form.get("draft_file")

        if not selected_module or not selected_file:
            flash("Please choose both a module and a draft file.", "error")
        else:
            input_path = (DRAFTS_DIR / selected_file).resolve()

            if not input_path.exists():
                flash(f"Draft file not found: {input_path}", "error")
            else:
                try:
                    compiled_prompt = build_prompt(
                        input_file=input_path,
                        module_name=selected_module,
                        config=PROMPT_CONFIG,
                        # override_output_path=None,
                        # debug=debug_enabled,  # for later
                    )
                    flash("Prompt compiled successfully.", "success")
                except PromptValidationError as e:
                    flash(f"Validation error: {e}", "error")
                except PromptConfigError as e:
                    flash(f"Configuration error: {e}", "error")
                except PromptError as e:
                    flash(str(e), "error")
                except Exception as e:
                    flash(f"Unexpected error: {e}", "error")

    return render_template(
        "index.html",
        draft_files=draft_files,
        modules=modules,
        compiled_prompt=compiled_prompt,
        selected_file=selected_file,
        selected_module=selected_module,
    )


if __name__ == "__main__":
    app.run(debug=True)
