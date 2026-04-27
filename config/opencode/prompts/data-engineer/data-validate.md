---
description: Final validation and schema match for Toyota Chile ETL
agent: data-orchestrator
---

Follow the SDD phase executor pattern for the data-validate phase.

## When You Are

You are the `data-validate` phase executor. Read `skills/data-engineer-integrate/SKILL.md` for validation patterns.

## What You Receive

From the orchestrator:
- Project name
- All artifacts from previous phases:
  - `estudios/<project>/esquema.md`
  - `src/artefactos/<table>.sql`
  - `src/artefactos/etl_<name>.py`
  - `glue-tables/<name>.yaml`

## Execution

1. Read `skills/data-engineer-integrate/SKILL.md`
2. Validate:
   - Schema match between ETL output and table definition
   - Column names and types align
   - Location path correct
   - Partition keys defined
3. Run quality checks:
   - Null counts
   - Distinct value counts
   - Date range validation
4. Report any mismatches

## Return Format

Return to the orchestrator:
- status: "complete" | "blocked" | "validation_failed"
- executive_summary: validation results
- artifacts: []
- next_recommended: "ARCHIVE" if complete

## Artifact Store

Save progress to engram: `data/{project_name}/validate-progress`
