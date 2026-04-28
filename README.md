# SDRF Templates

Versioned templates and validation rules for SDRF-Proteomics.

[![Validate Templates](https://github.com/bigbio/sdrf-templates/actions/workflows/validate-templates.yml/badge.svg?branch=main)](https://github.com/bigbio/sdrf-templates/actions/workflows/validate-templates.yml)
[![Generate Manifest](https://github.com/bigbio/sdrf-templates/actions/workflows/generate-manifest.yml/badge.svg?branch=main)](https://github.com/bigbio/sdrf-templates/actions/workflows/generate-manifest.yml)
[![License](https://img.shields.io/github/license/bigbio/sdrf-templates)](https://github.com/bigbio/sdrf-templates/blob/main/LICENSE)

## Overview

This repository stores versioned SDRF template definitions as YAML files. These templates are
used by the SDRF specification and validation tooling to define required columns, optional
columns, inheritance rules, and lightweight validation constraints for different experiment
types and sample metadata layers.

The repository is intentionally data-driven:

- Each template lives in its own versioned directory.
- `templates.yaml` provides the generated manifest of all known templates.
- Template inheritance is declared with `extends`.
- Validation CI checks YAML structure and manifest generation.

## Structure

```
{template-name}/
  {version}/
    {template-name}.yaml      # Validation rules and column definitions
```

## Manifest

The `templates.yaml` manifest is auto-generated on merge to `main`. It contains:
- All available templates
- Latest version for each template
- Version history
- Inheritance relationships (`extends`)

## Usage

### Finding the latest version

```python
import yaml

with open('templates.yaml') as f:
    manifest = yaml.safe_load(f)

# Get latest human template version
latest = manifest['templates']['human']['latest']  # e.g., "1.1.0"
```

### Loading a template

```python
from pathlib import Path
import yaml

def load_template(name: str, version: str = None) -> dict:
    if version is None:
        with open('templates.yaml') as f:
            manifest = yaml.safe_load(f)
        version = manifest['templates'][name]['latest']

    template_path = Path(name) / version / f'{name}.yaml'
    with open(template_path) as f:
        return yaml.safe_load(f)
```

## Template Inheritance

Templates use an `extends` field to inherit columns from parent templates:

- `base` - Infrastructure columns (source name, assay name, technology type, etc.)
- `sample-metadata` extends `base` - Sample-level columns shared by all templates (organism, organism part, cell type, biological replicate, pooled sample, disease, biosample accession)
- `ms-proteomics` extends `sample-metadata` - Mass spectrometry columns
- `ms-metabolomics` extends `sample-metadata` - Mass spectrometry-based metabolomics columns
- `affinity-proteomics` extends `sample-metadata` - Affinity assay columns
- `human` extends `sample-metadata` - Human sample columns
- `vertebrates` extends `sample-metadata` - Non-human vertebrate columns
- `invertebrates` extends `sample-metadata` - Invertebrate columns
- `plants` extends `sample-metadata` - Plant columns
- `dia-acquisition` extends `ms-proteomics` - DIA-specific columns
- `lc-ms-metabolomics` extends `ms-metabolomics` - LC-MS metabolomics columns
- `gc-ms-metabolomics` extends `ms-metabolomics` - GC-MS metabolomics columns

In practice, downstream tools should resolve parent templates transitively. Submitters normally
declare the most specific leaf templates rather than repeating all inherited parents.

## Adding a New Version

1. Create a new version directory: `{template-name}/{new-version}/`
2. Add `{template-name}.yaml` with updated `version` field
3. Submit a PR to the active development branch
4. Manifest will auto-update on merge

## Repositories Using This

- [proteomics-metadata-standard](https://github.com/bigbio/proteomics-sample-metadata) - Specification
- [sdrf-pipelines](https://github.com/bigbio/sdrf-pipelines) - Validator

## For LLMs

The repository now also includes [`llms.txt`](./llms.txt), a lightweight index of the files and
URLs that are most useful for LLM-assisted tooling and repository navigation.
