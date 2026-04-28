# SDRF Templates

Versioned templates and validation rules for SDRF-Proteomics.

## Structure

```
{template-name}/
  {version}/
    {template-name}.yaml      # Validation rules and column definitions
```

## Manifest

The `templates.yaml` manifest is auto-generated on merge to master. It contains:
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

## Adding a New Version

1. Create a new version directory: `{template-name}/{new-version}/`
2. Add `{template-name}.yaml` with updated `version` field
3. Submit PR to master
4. Manifest will auto-update on merge

## Repositories Using This

- [proteomics-metadata-standard](https://github.com/bigbio/proteomics-sample-metadata) - Specification
- [sdrf-pipelines](https://github.com/bigbio/sdrf-pipelines) - Validator
