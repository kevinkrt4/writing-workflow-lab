#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python}"
REPORT_DIR="${REPORT_DIR:-review_reports}"
TIMESTAMP="$(date '+%Y-%m-%d_%H%M%S')"
REPORT_PATH="${REPORT_DIR}/review_${TIMESTAMP}.md"
LATEST_REPORT_PATH="${REPORT_DIR}/latest.md"
STATUS="passed"
PYTHON_VERSION="$("$PYTHON_BIN" --version)"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

mkdir -p "$REPORT_DIR"

command_string() {
  printf '%q ' "$@"
}

capture_command() {
  "$@" 2>&1
}

git_value() {
  local fallback="$1"
  shift

  git "$@" 2>/dev/null || printf '%s\n' "$fallback"
}

git_dirty_status() {
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "unknown - not a git worktree"
    return
  fi

  if [[ -z "$(git status --porcelain)" ]]; then
    echo "clean"
  else
    echo "dirty"
  fi
}

append_command_block() {
  local label="$1"
  shift
  local output

  output="$(capture_command "$@")"
  {
    echo "### ${label}"
    echo
    echo '```text'
    printf '%s\n' "$output"
    echo '```'
    echo
  } >> "$REPORT_PATH"
}

write_tool_versions() {
  local ruff_version
  local black_version
  local isort_version
  local pytest_version

  ruff_version="$(capture_command "$PYTHON_BIN" -m ruff --version)"
  black_version="$(capture_command "$PYTHON_BIN" -m black --version)"
  isort_version="$(capture_command "$PYTHON_BIN" -m isort --version-number)"
  pytest_version="$(capture_command "$PYTHON_BIN" -m pytest --version)"

  {
    echo "## Tool Versions"
    echo
    echo '```text'
    echo "python: ${PYTHON_VERSION}"
    echo "ruff: ${ruff_version}"
    echo "black: ${black_version}"
    echo "isort: ${isort_version}"
    echo "pytest: ${pytest_version}"
    echo '```'
    echo
  } >> "$REPORT_PATH"
}

write_report_header() {
  {
    echo "# Writers Workbench Review Report"
    echo
    echo "- Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "- Report path: ${REPORT_PATH}"
    echo "- Project root: ${PROJECT_ROOT}"
    echo "- Invocation directory: $(pwd -P)"
    echo "- Python binary: ${PYTHON_BIN}"
    echo "- Python version: ${PYTHON_VERSION}"
    echo
    echo "## Git State"
    echo
    echo "- Branch: $(git_value unknown branch --show-current)"
    echo "- HEAD: $(git_value unknown rev-parse --short HEAD)"
    echo "- Upstream: $(git_value none rev-parse --abbrev-ref --symbolic-full-name '@{u}')"
    echo "- Worktree status: $(git_dirty_status)"
    echo
    echo "### Changed Files"
    echo
    echo '```text'
    git status --short 2>/dev/null || true
    echo '```'
    echo
  } > "$REPORT_PATH"
}

append_report_section() {
  local name="$1"
  local status="$2"
  local command="$3"
  local exit_code="$4"
  local output="$5"

  {
    echo "## ${name}"
    echo
    echo "Status: ${status}"
    echo
    echo "Command:"
    echo
    echo '```bash'
    printf '%s\n' "$command"
    echo '```'
    echo
    echo "Exit code: ${exit_code}"
    echo
    echo '```text'
    printf '%s\n' "$output"
    echo '```'
    echo
  } >> "$REPORT_PATH"
}

write_report_footer() {
  {
    echo "## Not Checked / Residual Risk"
    echo
    echo "- Browser-level UI behavior is not checked."
    echo "- Provider/API execution is not checked."
    echo "- Document coverage-map workflows are not checked yet."
    echo "- GitHub CI has not run this review command."
    echo "- Tests currently cover the existing prompt compiler and Flask smoke paths only."
    echo
    echo "## Result"
    echo
    echo "Status: ${STATUS}"
  } >> "$REPORT_PATH"
  cp "$REPORT_PATH" "$LATEST_REPORT_PATH"
}

write_report_header

echo "== Writers Workbench Review =="
echo "Python: $("$PYTHON_BIN" --version)"
echo "Report: ${REPORT_PATH}"
echo

run_step() {
  local name="$1"
  shift

  echo "== ${name} =="
  local output
  local step_status
  local command

  command="$(command_string "$@")"
  set +e
  output="$(capture_command "$@")"
  step_status=$?
  set -e

  printf '%s\n' "$output"

  if [[ "$step_status" -eq 0 ]]; then
    append_report_section "$name" "passed" "$command" "$step_status" "$output"
  else
    STATUS="failed"
    append_report_section "$name" "failed" "$command" "$step_status" "$output"
    write_report_footer
    echo
    echo "Review failed. Report written to: ${REPORT_PATH}"
    exit "$step_status"
  fi

  echo
}

write_tool_versions

run_step "ruff" "$PYTHON_BIN" -m ruff check .
run_step "black" "$PYTHON_BIN" -m black --check .
run_step "isort" "$PYTHON_BIN" -m isort --check-only .
run_step "pytest" "$PYTHON_BIN" -m pytest
run_step "architecture checks" "$PYTHON_BIN" tools/architecture_checks.py

write_report_footer

echo "Review passed."
echo "Report written to: ${REPORT_PATH}"
