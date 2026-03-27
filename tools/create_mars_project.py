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


def apply_placeholder_replacements(
    project_dir: Path, replacements: dict[str, str]
) -> None:
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


def resolve_ai_overlays(
    with_ai: bool,
    with_copilot: bool,
    with_opencode: bool,
) -> set[str]:
    """
    Resolve which AI overlays should be applied.

    Rules:
    - --with-ai copies both Copilot and OpenCode overlays.
    - --with-copilot copies only Copilot.
    - --with-opencode copies only OpenCode.
    - No AI flags means no AI overlays.
    """
    if with_ai:
        return {"copilot", "opencode"}

    selected: set[str] = set()

    if with_copilot:
        selected.add("copilot")

    if with_opencode:
        selected.add("opencode")

    return selected


def copy_overlay_contents(overlay_dir: Path, project_dir: Path) -> None:
    """
    Copy the contents of an overlay into the root of the target project.

    The overlay is expected to already contain the final relative paths
    (for example `.github/...` or `AGENTS.md`).
    """
    if not overlay_dir.exists():
        raise FileNotFoundError(f"Overlay directory not found: {overlay_dir}")

    if not overlay_dir.is_dir():
        raise NotADirectoryError(f"Overlay path is not a directory: {overlay_dir}")

    for source_path in overlay_dir.rglob("*"):
        relative_path = source_path.relative_to(overlay_dir)
        destination_path = project_dir / relative_path

        if source_path.is_dir():
            destination_path.mkdir(parents=True, exist_ok=True)
            continue

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        if destination_path.exists():
            raise FileExistsError(
                f"Overlay copy would overwrite an existing file: {destination_path}"
            )

        shutil.copy2(source_path, destination_path)


def apply_ai_overlays(
    project_dir: Path,
    mars_root: Path,
    selected_overlays: set[str],
    replacements: dict[str, str],
) -> None:
    """
    Apply selected AI overlays to the project and replace placeholders inside them.
    """
    if not selected_overlays:
        return

    overlays_root = mars_root / "overlays" / "ai"

    overlay_map = {
        "copilot": overlays_root / "copilot",
        "opencode": overlays_root / "opencode",
    }

    for overlay_name in sorted(selected_overlays):
        overlay_dir = overlay_map[overlay_name]
        copy_overlay_contents(overlay_dir, project_dir)

    apply_placeholder_replacements(project_dir, replacements)


def create_project(
    name: str,
    destination: Path,
    with_ai: bool = False,
    with_copilot: bool = False,
    with_opencode: bool = False,
) -> Path:
    """
    Create a new project from the MARS template and optional overlays.
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

    selected_ai_overlays = resolve_ai_overlays(
        with_ai=with_ai,
        with_copilot=with_copilot,
        with_opencode=with_opencode,
    )

    apply_ai_overlays(
        project_dir=project_dir,
        mars_root=mars_root,
        selected_overlays=selected_ai_overlays,
        replacements=replacements,
    )

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
    parser.add_argument(
        "--with-ai",
        action="store_true",
        help="Include both Copilot and OpenCode AI overlays.",
    )
    parser.add_argument(
        "--with-copilot",
        action="store_true",
        help="Include only the Copilot overlay.",
    )
    parser.add_argument(
        "--with-opencode",
        action="store_true",
        help="Include only the OpenCode overlay.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    project_dir = create_project(
        name=args.name,
        destination=Path(args.destination),
        with_ai=args.with_ai,
        with_copilot=args.with_copilot,
        with_opencode=args.with_opencode,
    )

    print(f"Project created successfully at: {project_dir}")


if __name__ == "__main__":
    main()
