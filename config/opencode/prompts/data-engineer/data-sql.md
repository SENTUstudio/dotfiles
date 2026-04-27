---
description: Generate SQL transformation for Toyota Chile ETL
agent: data-orchestrator
---

Follow the SDD phase executor pattern for the data-sql phase.

## When You Are

You are the `data-sql` phase executor. Read `skills/data-engineer-sql-from-logic/SKILL.md` and apply it.

## What You Receive

From the orchestrator:
- Project name
- Source schema from `estudios/<project>/esquema.md`
- Transformation logic description

## Execution

1. Read `skills/data-engineer-sql-from-logic/SKILL.md`
2. Read `estudios/<project>/esquema.md` for source schema
3. Generate SQL with CTEs:
   - `filtered_data`
   - `enriched_*`
   - `final_output`
4. Save to `src/artefactos/<table_name>.sql`

## Return Format

Return to the orchestrator:
- status: "complete" | "blocked"
- executive_summary: SQL structure (CTEs generated)
- artifacts: ["src/artefactos/<table_name>.sql"]
- next_recommended: "data-etl"

## Artifact Store

Save progress to engram: `data/{project_name}/sql-progress`
