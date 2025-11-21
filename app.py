from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
import subprocess

app = Flask(__name__)
app.secret_key = "change-me"

# Path to your draft notebook files
WORKFLOWS_DIR = Path.home() / "Documents" / "GitHub" / "webwork" / "drafts"

MODULES = [
    ("narrative", "001 - Narrative Synopsis"),
    ("outline", "002 - Outline Synopsis"),
    ("characters", "003 - Characters & Relationships"),
    ("synthesis", "012 - Synthesis"),
]


def list_available_files():
    """Return .txt and .md files in the WORKFLOWS_DIR directory."""
    if not WORKFLOWS_DIR.exists():
        return []

    files = []
    files.extend(WORKFLOWS_DIR.glob("*.txt"))
    files.extend(WORKFLOWS_DIR.glob("*.md"))

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

        input_path = (WORKFLOWS_DIR / input_file).resolve()

        if not input_path.exists():
            flash(f"Input file not found: {input_path}")
            return redirect(url_for("index"))

        cmd = [
            "python3",
            "preprocess_prompt.py"
        ]
        if debug_enabled:              # NEW
            cmd.append("--debug")
        #,
        #    "--module",
        #    module,
        #    "--input",
        #    str(input_path),
        #]

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
