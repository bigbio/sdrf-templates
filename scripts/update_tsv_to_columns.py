#!/usr/bin/env python3
"""
Update TSV template files from header-based to column-based metadata.

Removes header comments (#file_format, #version, #template) and adds
metadata columns (comment[sdrf version], comment[sdrf template], etc.)
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# Templates to update
TEMPLATES = [
    "base",
    "human",
    "vertebrates",
    "invertebrates",
    "plants",
    "cell-lines",
    "single-cell",
    "ms-proteomics",
    "affinity-proteomics",
    "dda-acquisition",
    "dia-acquisition",
    "crosslinking",
    "immunopeptidomics",
    "metaproteomics",
    "olink",
    "somascan",
]


def find_tsv_file(template_name: str) -> Path | None:
    """Find the TSV file for a template."""
    template_dir = REPO_ROOT / template_name
    if not template_dir.exists():
        return None

    for version_dir in template_dir.iterdir():
        if version_dir.is_dir():
            tsv_file = version_dir / f"{template_name}.sdrf.tsv"
            if tsv_file.exists():
                return tsv_file
    return None


def parse_headers(content: str) -> dict:
    """Parse header lines and extract metadata."""
    metadata = {
        "version": "v1.1.0",
        "templates": [],
    }

    lines = content.split("\n")
    for line in lines:
        if line.startswith("#"):
            # Parse #key=value format
            match = re.match(r"#(\w+)=(.+)", line)
            if match:
                key, value = match.groups()
                if key == "version":
                    metadata["version"] = value
                elif key == "template":
                    metadata["templates"].append(value)

    return metadata


def update_tsv_file(tsv_path: Path, template_name: str) -> bool:
    """Update a TSV file from header-based to column-based metadata."""
    with open(tsv_path, encoding="utf-8") as f:
        content = f.read()

    # Parse existing headers
    metadata = parse_headers(content)

    # Find the header row (first non-comment, non-empty line)
    lines = content.split("\n")
    header_line = None
    header_idx = 0

    for i, line in enumerate(lines):
        if line.strip() and not line.startswith("#"):
            header_line = line
            header_idx = i
            break

    if header_line is None:
        print(f"  ERROR: No header row found in {tsv_path}")
        return False

    # Parse existing columns
    columns = header_line.split("\t")

    # Check if metadata columns already exist
    has_version = any("comment[sdrf version]" in col for col in columns)
    has_template = any("comment[sdrf template]" in col for col in columns)
    has_tool = any("comment[sdrf annotation tool]" in col for col in columns)

    # Add metadata columns if not present
    new_columns = columns.copy()
    if not has_version:
        new_columns.append("comment[sdrf version]")
    if not has_template:
        # Add template columns
        if metadata["templates"]:
            for _ in metadata["templates"]:
                new_columns.append("comment[sdrf template]")
        else:
            new_columns.append("comment[sdrf template]")
    if not has_tool:
        new_columns.append("comment[sdrf annotation tool]")

    # Create new header line
    new_header_line = "\t".join(new_columns)

    # Get remaining lines (skip header comments and old header)
    data_lines = lines[header_idx + 1:]

    # Write updated file (no header comments)
    with open(tsv_path, "w", encoding="utf-8") as f:
        f.write(new_header_line + "\n")
        for line in data_lines:
            if line.strip():  # Skip empty lines
                f.write(line + "\n")

    return True


def main():
    print("Updating TSV templates to column-based metadata...")
    print("-" * 60)

    updated = 0
    for template_name in TEMPLATES:
        tsv_path = find_tsv_file(template_name)
        if tsv_path is None:
            print(f"SKIP: {template_name} - no TSV file found")
            continue

        print(f"Updating: {tsv_path.relative_to(REPO_ROOT)}")
        if update_tsv_file(tsv_path, template_name):
            updated += 1

    print("-" * 60)
    print(f"Updated {updated} TSV files")


if __name__ == "__main__":
    main()
