#!/usr/bin/env python3
"""
Migrate templates from proteomics-metadata-standard to sdrf-templates.
Creates versioned directory structure: {template-name}/{version}/{files}
"""

import os
import shutil
import yaml
from pathlib import Path

# Paths
SOURCE_DIR = Path("/Users/yperez/work/proteomics-metadata-standard/sdrf-proteomics/templates")
TARGET_DIR = Path("/Users/yperez/work/sdrf-templates")

# Templates to migrate (directory names)
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


def migrate_template(template_name: str) -> dict:
    """Migrate a single template and return its metadata."""
    source_template_dir = SOURCE_DIR / template_name
    yaml_file = source_template_dir / f"{template_name}.yaml"
    tsv_file = source_template_dir / f"{template_name}-template.sdrf.tsv"

    if not yaml_file.exists():
        print(f"  WARNING: {yaml_file} not found, skipping")
        return None

    # Read YAML to get version
    with open(yaml_file) as f:
        template_data = yaml.safe_load(f)

    version = template_data.get("version", "1.0.0")
    extends = template_data.get("extends")

    # Create versioned directory
    target_version_dir = TARGET_DIR / template_name / version
    target_version_dir.mkdir(parents=True, exist_ok=True)

    # Copy YAML file (renamed to {template-name}.yaml)
    target_yaml = target_version_dir / f"{template_name}.yaml"
    shutil.copy2(yaml_file, target_yaml)
    print(f"  Copied {yaml_file.name} -> {target_yaml.relative_to(TARGET_DIR)}")

    # Copy TSV file if exists (renamed to {template-name}.sdrf.tsv)
    if tsv_file.exists():
        target_tsv = target_version_dir / f"{template_name}.sdrf.tsv"
        shutil.copy2(tsv_file, target_tsv)
        print(f"  Copied {tsv_file.name} -> {target_tsv.relative_to(TARGET_DIR)}")
    else:
        print(f"  NOTE: No TSV template file for {template_name}")

    return {
        "name": template_name,
        "version": version,
        "extends": extends,
    }


def main():
    print("Migrating templates from proteomics-metadata-standard to sdrf-templates")
    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print("-" * 60)

    migrated = []
    for template_name in TEMPLATES:
        print(f"\nMigrating: {template_name}")
        result = migrate_template(template_name)
        if result:
            migrated.append(result)

    print("\n" + "=" * 60)
    print(f"Successfully migrated {len(migrated)} templates:")
    for t in migrated:
        extends_str = f" (extends: {t['extends']})" if t['extends'] else ""
        print(f"  - {t['name']} v{t['version']}{extends_str}")


if __name__ == "__main__":
    main()
