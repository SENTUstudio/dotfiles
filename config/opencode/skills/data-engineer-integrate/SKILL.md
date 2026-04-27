---
name: data-engineer-integrate
description: >
  Orchestrates all data engineering skills and manages the complete Toyota Chile ETL project lifecycle.
  Trigger: When orchestrating complete Toyota Chile ETL project.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- When starting a new Toyota Chile ETL project from scratch
- When managing an existing ETL project through its full lifecycle
- When coordinating multiple source systems and transformations
- During `sdd-propose` or `sdd-explore` phases for full project setup
- As master orchestrator that invokes other data-engineer-* skills

## Critical Patterns

### Project Lifecycle Flow

```
1. PROJECT SETUP
   └── Create project structure in estudios/<project_name>/
       ├── config/dev.yaml, config/prd.yaml
       └── src/artefactos/ folder

2. SOURCE ANALYSIS (runs data-engineer-study-file)
   └── Analyze all source files
       ├── Encoding, delimiter, date formats
       └── Generate cleaning rules

3. SQL GENERATION (runs data-engineer-sql-from-logic)
   └── If no SQL provided by source system
       ├── Generate transformation SQL
       └── Save to src/artefactos/<name>.sql

4. ETL SELECTION (triggers appropriate etl-* skill)
   ├── S3 source → data-engineer-etl-s3
   ├── Glue Catalog → data-engineer-etl-glue
   └── SharePoint → data-engineer-etl-sharepoint

5. TABLE CREATION (runs data-engineer-create-table)
   ├── Phase 1: ETL schema extraction
   ├── Phase 2: INFRA table definition
   └── Phase 3: Enable writes

6. QUALITY CHECKS
   ├── Validate schema match
   ├── Test in dev environment
   └── Document any deviations
```

### Project Structure

```
estudios/
├── config/                # Shared config (sibling to all projects)
│   ├── dev.yaml           # Dev environment variables
│   └── prd.yaml           # Production environment variables
├── <nombre_proyecto>/
│   ├── dev_<proyecto>.py   # Dev ETL entry point
│   ├── prd_<proyecto>.py   # Production ETL entry point
│   ├── input/              # Source files (gitignored)
│   ├── output/             # ETL output
│   │   ├── Quicksight/     # QuickSight-ready output
│   │   └── dev/            # Dev output for testing
│   ├── versions/           # Version history of ETL runs
│   ├── error_files.ipynb   # Jupyter notebook for error investigation
│   └── esquema.md          # Schema documentation
└── docs/
    ├── arquitectura/
    ├── datos/
    └── migracion/
```

### Skill Invocation Pattern

When integrating multiple skills, follow this invocation order:

1. **First**: `data-engineer-study-file` for all source files
   - Document encoding, delimiters, date formats
   - Produce cleaning rules

2. **Second**: `data-engineer-sql-from-logic` if no SQL provided
   - Generate SQL for each transformation step
   - Save to `src/artefactos/` folder

3. **Third**: Select appropriate etl-* skill based on source type
   - S3 → `data-engineer-etl-s3`
   - Glue Catalog → `data-engineer-etl-glue`
   - SharePoint → `data-engineer-etl-sharepoint`

4. **Fourth**: `data-engineer-create-table` through all phases
   - Phase 1: Schema extraction
   - Phase 2: INFRA YAML
   - Phase 3: Enable writes

## Code Examples

### Project Setup Script

```python
#!/usr/bin/env python3
"""Setup new Toyota Chile ETL project."""

from pathlib import Path
import yaml

PROJECT_NAME = "mi_proyecto"

def create_project_structure(base_path: str, project_name: str):
    """Create project directory structure."""
    base = Path(base_path)
    project_dir = base / project_name
    
    directories = [
        project_dir / "input",
        project_dir / "output" / "Quicksight",
        project_dir / "output" / "dev",
        project_dir / "versions",
        base / "config",
        base / "docs" / "arquitectura",
        base / "docs" / "datos",
        base / "docs" / "migracion",
    ]
    
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py files
    (base / "config" / "__init__.py").touch()
    (base / "__init__.py").touch()
    
    # Create skeleton files
    import json
    nb = {"nbformat": 4, "nbformat_minor": 4, "metadata": {}, "cells": []}
    (project_dir / "error_files.ipynb").write_text(json.dumps(nb, indent=1))
    (project_dir / "esquema.md").write_text("# Schema Documentation\n\n## Tables\n\n## Columns\n")
    
    # Create config files (shared by all projects)
    dev_config = {
        "environment": "dev",
        "BUCKET_RAW": "toyota-chile-raw-data-dev",
        "BUCKET_STG": "toyota-chile-refined-dev",
        "GLUE_DATABASE": "toyota_chile_dev",
        "ENCODING": "latin-1",
    }

    prd_config = {
        "environment": "prd",
        "BUCKET_RAW": "toyota-chile-raw-data",
        "BUCKET_STG": "toyota-chile-refined",
        "GLUE_DATABASE": "toyota_chile",
        "ENCODING": "latin-1",
    }
    
    with open(base / "config" / "dev.yaml", "w") as f:
        yaml.dump(dev_config, f)
    
    with open(base / "config" / "prd.yaml", "w") as f:
        yaml.dump(prd_config, f)
    
    # Create entry point templates
    dev_entry = f'''"""Dev ETL entry point for {project_name}."""
from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).parent / "config" / "dev.yaml"

def main():
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)
    print(f"Running dev ETL: {{config['environment']}}")

if __name__ == "__main__":
    main()
'''
    
    with open(base / f"dev_{project_name}.py", "w") as f:
        f.write(dev_entry)
    
    print(f"Project created at: {base}")

if __name__ == "__main__":
    import sys
    create_project_structure(sys.argv[1] if len(sys.argv) > 1 else ".", PROJECT_NAME)
```

### Integration Flow Example

```python
"""Example: Full ETL project lifecycle integration."""

# Step 1: Project setup
print("=== STEP 1: Project Setup ===")
# Run create_project_structure() or manual setup

# Step 2: Source analysis
print("=== STEP 2: Source Analysis ===")
# Run data-engineer-study-file for each source file
source_analysis = [
    {"file": "ventas.csv", "encoding": "latin-1", "delimiter": ";", "date_format": "DD/MM/YYYY"},
    {"file": "clientes.csv", "encoding": "UTF-8", "delimiter": ";", "date_format": "YYYY-MM-DD"},
]

# Step 3: SQL generation (if needed)
print("=== STEP 3: SQL Generation ===")
# Run data-engineer-sql-from-logic for transformations
# Output: src/artefactos/ventas_enriched.sql

# Step 4: ETL selection and generation
print("=== STEP 4: ETL Generation ===")
# Based on source_analysis, determine ETL type:
# - ventas.csv → S3 → data-engineer-etl-s3
# - clientes.csv from SharePoint → data-engineer-etl-sharepoint

# Step 5: Table creation (Phase 1: schema extraction)
print("=== STEP 5: Phase 1 - Schema Extraction ===")
# Generate ETL with commented writes
# Run and capture: df.printSchema()

# Step 6: Table creation (Phase 2: INFRA definition)
print("=== STEP 6: Phase 2 - INFRA Table Definition ===")
# Create glue-tables/<name>.yaml
# Deploy INFRA stack

# Step 7: Table creation (Phase 3: enable writes)
print("=== STEP 7: Phase 3 - Enable Writes ===")
# Uncomment write blocks
# Deploy CARGA stack

print("=== Project Complete ===")
```

## Commands

### Create New Project

```bash
# In gentle-ai repo, run:
python scripts/create_etl_project.py mi_proyecto

# Or manually:
mkdir -p estudios/mi_proyecto/{config,input,output/Quicksight,output/dev,versions,docs}
touch estudios/mi_proyecto/config/__init__.py
```

### Run Full Integration

```bash
# Execute integration flow
python -c "
from data_engineer_integrate import run_integration
run_integration('mi_proyecto', source_type='s3')
"
```

### Validate Project Structure

```bash
# Check project structure
tree estudios/mi_proyecto/

# Validate configs
python -c "
import yaml
with open('estudios/mi_proyecto/config/dev.yaml') as f:
    print(yaml.safe_load(f))
"
```

## Output

The skill produces:
- **Complete project structure** in `estudios/<project_name>/`
- **Config files** for dev and prd environments
- **ETL scripts** in `src/artefactos/` (reference copies)
- **Glue Jobs** in CARGA repo
- **Glue Tables** in INFRA repo
- **Documentation** in `docs/` subdirectories

## Resources

- **Toyota Chile ETL Template**: See external `toyota-chile-etl-template/` artifact for complete reference structure
- **Integration with other skills**:
  - `data-engineer-study-file` — source analysis
  - `data-engineer-sql-from-logic` — SQL generation
  - `data-engineer-etl-s3` — S3 ETL
  - `data-engineer-etl-glue` — Glue Catalog ETL
  - `data-engineer-etl-sharepoint` — SharePoint ETL
  - `data-engineer-create-table` — table creation workflow