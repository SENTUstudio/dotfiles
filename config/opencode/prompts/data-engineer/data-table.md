---
description: Create Glue table through 3-phase workflow
agent: data-orchestrator
---

## When You Are

You are the `data-table` phase executor. This has 3 sub-phases.

## Correct CARGA/INFRA Paths

```
CARGA repo:  migracion/PAP/carga-datos-stg-encuestas/
INFRA repo:  migracion/PAP/infra-datos-stg-encuestas/
ETL script:  src/artefactos/etl_<project>.py
Glue table:  migracion/PAP/infra-datos-stg-encuestas/glue-tables/<project>.yaml
```

## What You Receive

From the orchestrator:
- Project name
- ETL script: `src/artefactos/etl_<project>.py`
- Schema from `estudios/<project>/esquema.md`

## Execution

### Phase 1: Schema Extraction (CARGA)

1. Read ETL script at `src/artefactos/etl_<project>.py`
2. Comment out write sections (leave only read + transform)
3. Add `df_final.printSchema()` at end
4. Copy to `migracion/PAP/carga-datos-stg-encuestas/glue-jobs/<project>_schema.py`
5. Commit to CARGA repo

### Phase 2: INFRA Definition

1. Read `skills/data-engineer-create-table/SKILL.md`
2. Create CloudFormation YAML at `migracion/PAP/infra-datos-stg-encuestas/glue-tables/<project>.yaml`:
   - `Type: EXTERNAL_TABLE` inside `TableInput` (NOT Properties level)
   - `Description: !Sub "Stage ${AWS::StackName} <description>"`
   - StorageDescriptor with columns from schema
   - Location: `s3://<bucket>/<project>/`
3. Deploy: `aws cloudformation deploy`
4. Commit to INFRA repo

### Phase 3: Enable Writes

1. Uncomment write sections in ETL script
2. Add `job.commit()` before exit
3. Copy final version to `migracion/PAP/carga-datos-stg-encuestas/glue-jobs/<project>.py`
4. Commit to CARGA repo

## Return Format

Return to the orchestrator:
- status: "complete" | "blocked"
- executive_summary: which phase(s) completed
- artifacts: ["migracion/PAP/.../glue-tables/<project>.yaml", "migracion/PAP/.../glue-jobs/<project>.py"]
- next_recommended: "data-validate"

## Artifact Store

Save progress to engram: `data/{project}/table-progress`
