from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

TEXT_FILE_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".gitignore",
}

EMPTY_NOTEBOOK = {
    "cells": [],
    "metadata": {},
    "nbformat": 4,
    "nbformat_minor": 5,
}


def make_project_slug(name: str) -> str:
    """
    Convert a project name into a filesystem-friendly slug.
    Example:
        "Titan Risk Modeling" -> "titan-risk-modeling"
    """
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")

    if not slug:
        raise ValueError("Project name produced an empty slug.")

    return slug


def replace_placeholders_in_text(file_path: Path, replacements: dict[str, str]) -> None:
    """
    Replace template placeholders inside a text file.
    Silently skips files that cannot be decoded as UTF-8 text.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    file_path.write_text(content, encoding="utf-8")


def should_treat_as_text(file_path: Path) -> bool:
    """
    Decide whether a file should be processed for placeholder replacement.
    """
    return file_path.suffix in TEXT_FILE_EXTENSIONS or file_path.name == ".gitignore"


def copy_template_to_project(template_dir: Path, project_dir: Path) -> None:
    """
    Copy the full template directory into the new project directory.
    """
    shutil.copytree(template_dir, project_dir)


def apply_placeholder_replacements(project_dir: Path, replacements: dict[str, str]) -> None:
    """
    Walk through copied files and replace placeholders in text files.
    """
    for path in project_dir.rglob("*"):
        if path.is_file() and should_treat_as_text(path):
            replace_placeholders_in_text(path, replacements)


def create_notebook_if_missing(notebook_path: Path) -> None:
    """
    Create a minimal valid Jupyter notebook if it does not already exist.
    """
    if notebook_path.exists():
        return

    notebook_path.parent.mkdir(parents=True, exist_ok=True)
    notebook_path.write_text(
        json.dumps(EMPTY_NOTEBOOK, indent=2),
        encoding="utf-8",
    )


def create_default_notebooks(project_dir: Path) -> None:
    """
    Create the default project notebooks if they are missing.
    """
    notebooks_dir = project_dir / "notebooks"

    create_notebook_if_missing(notebooks_dir / "01_eda.ipynb")
    create_notebook_if_missing(notebooks_dir / "02_modeling.ipynb")


def create_project(name: str, destination: Path) -> Path:
    """
    Create a new project from the MARS template.
    """
    script_path = Path(__file__).resolve()
    mars_root = script_path.parent.parent
    template_dir = mars_root / "template"

    if not template_dir.exists():
        raise FileNotFoundError(f"Template directory not found: {template_dir}")

    if not template_dir.is_dir():
        raise NotADirectoryError(f"Template path is not a directory: {template_dir}")

    project_name = name.strip()
    if not project_name:
        raise ValueError("Project name cannot be empty.")

    project_slug = make_project_slug(project_name)

    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)

    project_dir = destination / project_slug

    if project_dir.exists():
        raise FileExistsError(f"Project directory already exists: {project_dir}")

    copy_template_to_project(template_dir, project_dir)

    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROJECT_SLUG}}": project_slug,
    }

    apply_placeholder_replacements(project_dir, replacements)
    create_default_notebooks(project_dir)

    return project_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new MARS project from the template."
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Human-readable project name, e.g. 'Titan Risk Modeling'.",
    )
    parser.add_argument(
        "--destination",
        required=True,
        help="Parent directory where the new project folder will be created.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_dir = create_project(
        name=args.name,
        destination=Path(args.destination),
    )
    print(f"Project created successfully at: {project_dir}")


if __name__ == "__main__":
    main()
