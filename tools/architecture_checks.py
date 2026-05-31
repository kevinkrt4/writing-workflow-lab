#!/usr/bin/env python3
"""Project-specific structural checks for Writers Workbench."""

from __future__ import annotations

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PATHS = [
    "app.py",
    "config/prompt_config.yaml",
    "prompts/compiler_TEMPLATE_v1.9d.txt",
    "specs/Prompt_Execution_Spec_v0.2.3.md",
    "tools/preprocess_prompt.py",
]

PROVIDER_MODULES = {
    "anthropic",
    "cohere",
    "google.generativeai",
    "litellm",
    "openai",
}

PROVIDER_ADAPTER_DIRS = {
    "adapters",
    "providers",
}

SOURCE_DIRS = {
    "tests",
    "tools",
}

SOURCE_FILES = {
    "app.py",
}


def iter_python_files() -> list[Path]:
    files: list[Path] = []

    for source_file in SOURCE_FILES:
        path = PROJECT_ROOT / source_file
        if path.exists():
            files.append(path)

    for source_dir in SOURCE_DIRS:
        root = PROJECT_ROOT / source_dir
        if root.exists():
            files.extend(sorted(root.rglob("*.py")))

    return sorted(set(files))


def module_root(module_name: str) -> str:
    return module_name.split(".", 1)[0]


def is_provider_import(module_name: str) -> bool:
    module_roots = {module_root(name) for name in PROVIDER_MODULES}
    return module_root(module_name) in module_roots


def is_provider_adapter(path: Path) -> bool:
    relative_parts = path.relative_to(PROJECT_ROOT).parts
    return any(part in PROVIDER_ADAPTER_DIRS for part in relative_parts)


def imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)

    return modules


def check_required_paths() -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_PATHS:
        if not (PROJECT_ROOT / relative_path).exists():
            errors.append(f"Required project path is missing: {relative_path}")

    return errors


def check_provider_import_boundaries() -> list[str]:
    errors: list[str] = []

    for path in iter_python_files():
        if is_provider_adapter(path):
            continue

        for module_name in imported_modules(path):
            if is_provider_import(module_name):
                relative = path.relative_to(PROJECT_ROOT)
                errors.append(
                    f"Provider import outside adapter boundary: {relative} imports "
                    f"{module_name}"
                )

    return errors


def check_flask_route_boundaries() -> list[str]:
    errors: list[str] = []
    app_path = PROJECT_ROOT / "app.py"

    if not app_path.exists():
        return errors

    imported = imported_modules(app_path)
    for module_name in imported:
        if is_provider_import(module_name):
            errors.append(f"Flask route layer imports provider SDK: {module_name}")

    return errors


def run_checks() -> list[str]:
    errors: list[str] = []
    errors.extend(check_required_paths())
    errors.extend(check_provider_import_boundaries())
    errors.extend(check_flask_route_boundaries())
    return errors


def main() -> int:
    errors = run_checks()

    if errors:
        print("Architecture checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Architecture checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
