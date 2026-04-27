---
description: Build ETL pipeline for Toyota Chile ETL project
agent: data-orchestrator
---

## When You Are

You are the `data-etl` phase executor.

## What You Receive

From the orchestrator:
- Project name
- Source type (S3 | Glue | SharePoint)
- Schema from `estudios/<project>/esquema.md`

## Correct Paths

```
Source:      estudios/<project>/input/<file>.csv
Output S3:   s3://<bucket>/<project>/
ETL script:  src/artefactos/etl_<project>.py
```

## Execution

1. Read schema from `estudios/<project>/esquema.md`
2. Select ETL skill based on source type:
   - S3 → `skills/data-engineer-etl-s3/SKILL.md`
   - Glue Catalog → `skills/data-engineer-etl-glue/SKILL.md`
   - SharePoint → `skills/data-engineer-etl-sharepoint/SKILL.md`

3. Generate `src/artefactos/etl_<project>.py` with:
   - **Watermark pattern**: `get_last_load_timestamp()` → incremental
   - **Glue Job lifecycle**: `job.init()`, `job.commit()`
   - **Encoding**: latin-1 (from study-file)
   - **Delimiter**: semicolon
   - **Partition**: year, month, day

4. Also create:
   - `estudios/<project>/dev_<project>.py` — dev entry point
   - `estudios/<project>/prd_<project>.py` — prd entry point

## Return Format

Return to the orchestrator:
- status: "complete" | "blocked"
- executive_summary: ETL pattern, source/destination
- artifacts: ["src/artefactos/etl_<project>.py", "estudios/<project>/dev_<project>.py", "estudios/<project>/prd_<project>.py"]
- next_recommended: "data-table"

## Artifact Store

Save progress to engram: `data/{project}/etl-progress`
