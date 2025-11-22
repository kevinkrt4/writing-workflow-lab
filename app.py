import subprocess
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "change-me"

# -------------------------------------------------------------
# Draft notebooks live inside this repo: writing-workflow-lab/drafts
# -------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
DRAFTS_DIR = APP_DIR / "drafts"
# -------------------------------------------------------------

MODULES = [
    ("narrative", "001 - Narrative Synopsis"),
    ("outline", "002 - Outline Synopsis"),
    ("characters", "003 - Characters & Relationships"),
    ("synthesis", "012 - Synthesis"),
]


def list_available_files():
    """Return .txt and .md files in the DRAFTS_DIR directory."""
    if not DRAFTS_DIR.exists():
        return []

    files = []
    files.extend(DRAFTS_DIR.glob("*.txt"))

    return sorted([p.name for p in files], key=str)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        module = request.form.get("module")
        input_file = request.form.get("input_file")
        debug_enabled = bool(request.form.get("debug"))  # NEW

        if not module or not input_file:
            flash("Please choose both a module and an input file.")
            return redirect(url_for("index"))

        input_path = (DRAFTS_DIR / input_file).resolve()

        if not input_path.exists():
            flash(f"Input file not found: {input_path}")
            return redirect(url_for("index"))

        cmd = ["python3", "preprocess_prompt.py"]
        if debug_enabled:  # NEW
            cmd.append("--debug")
        # ,
        #    "--module",
        #    module,
        #    "--input",
        #    str(input_path),
        # ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            logs = result.stdout
            flash("Module ran successfully.")
        except subprocess.CalledProcessError as e:
            logs = (e.stdout or "") + "\n" + (e.stderr or "")
            flash("Error running module.")

        return render_template(
            "index.html",
            modules=MODULES,
            files=list_available_files(),
            logs=logs,
        )

    # GET: return the page
    return render_template(
        "index.html",
        modules=MODULES,
        files=list_available_files(),
        logs=None,
    )


if __name__ == "__main__":
    app.run(debug=True)
