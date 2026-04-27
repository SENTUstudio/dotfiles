---
description: Create new Toyota Chile ETL project structure
agent: data-orchestrator
---

## Project Structure (CORRECT)

```
estudios/
├── <proyecto>/           # uno por proyecto (avance_cotizantes, avance_dyp, etc.)
│   ├── input/           # archivos fuente
│   ├── output/          # archivos salida
│   │   └── Quicksight/
│   ├── versions/        # versiones del script
│   ├── __pycache__/
│   ├── __init__.py
│   ├── dev_<proyecto>.py      # script dev
│   └── prd_<proyecto>.py      # script prd
├── config/               # COMPARTIDO, no dentro del proyecto
│   ├── dev.yaml
│   └── prd.yaml
src/
└── artefactos/          # ETL scripts
    └── etl_<nombre>.py
migracion/PAP/
├── carga-datos-stg-encuestas/   # CARGA repo
│   ├── README.md
│   ├── template.yaml
│   └── glue-jobs/
└── infra-datos-stg-encuestas/   # INFRA repo
    ├── README.md
    ├── template.yaml
    └── glue-tables/
```

## When You Are

You are the `data-setup` phase executor.

## What You Receive

From the orchestrator:
- Project name (e.g., "avance_cotizantes")
- Source type (S3 | Glue | SharePoint)

## Execution

Create ONLY these directories/files:

1. `estudios/<project>/input/` — empty, source files go here
2. `estudios/<project>/output/Quicksight/` — empty
3. `estudios/<project>/versions/` — empty
4. `estudios/<project>/__init__.py` — empty file
5. `estudios/<project>/esquema.md` — skeleton with headers only
6. `estudios/<project>/error_files.ipynb` — valid JSON notebook
7. `estudios/config/dev.yaml` — if not exists
8. `estudios/config/prd.yaml` — if not exists

DO NOT create:
- `estudios/config/` inside project — it's shared at `estudios/config/`
- `dev_*.py` or `prd_*.py` — those are created by data-etl phase
- `src/artefactos/` — that's existing, not created per project

## Return Format

Return to the orchestrator:
- status: "complete" | "blocked"
- executive_summary: structure created
- artifacts: list of paths created
- next_recommended: "data-study"

## Artifact Store

Save progress to engram: `data/{project}/setup-progress`
