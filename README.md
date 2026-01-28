# SDRF Templates

Versioned templates and validation rules for SDRF-Proteomics.

## Structure

```
{template-name}/
  {version}/
    {template-name}.yaml      # Validation rules and column definitions
    {template-name}.sdrf.tsv  # Example template file
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

- `base` - Core columns shared by all templates
- `ms-proteomics` extends `base` - Mass spectrometry columns
- `affinity-proteomics` extends `base` - Affinity assay columns
- `human` extends `base` - Human sample columns
- `dda-acquisition` extends `ms-proteomics` - DDA-specific columns

## Adding a New Version

1. Create a new version directory: `{template-name}/{new-version}/`
2. Add `{template-name}.yaml` with updated `version` field
3. Add `{template-name}.sdrf.tsv` example file
4. Submit PR to master
5. Manifest will auto-update on merge

## Repositories Using This

- [proteomics-metadata-standard](https://github.com/bigbio/proteomics-sample-metadata) - Specification
- [sdrf-pipelines](https://github.com/bigbio/sdrf-pipelines) - Validator
