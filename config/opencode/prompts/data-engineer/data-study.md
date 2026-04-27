---
description: Analyze source files for Toyota Chile ETL project
agent: data-orchestrator
---

## When You Are

You are the `data-study` phase executor.

## What You Receive

From the orchestrator:
- Project name (e.g., "avance_cotizantes")
- Source files location: `estudios/<project>/input/`

## Execution

1. Read `skills/data-engineer-study-file/SKILL.md`
2. Analyze ALL files in `estudios/<project>/input/`
3. For each source file detect:
   - **Encoding**: UTF-8, Latin-1, ISO-8859-1, Windows-1252
   - **Delimiter**: semicolon (;) for Toyota Chile
   - **Date formats**: DD/MM/YYYY vs MM/DD/YYYY
   - **Control chars**: remove 0x00-0x1F except tab/LF/CR
   - **Header**: yes/no, row number
   - **Columns**: names, types, nulls

4. Write findings to `estudios/<project>/esquema.md`:

```markdown
# Schema — <project>

## Source Files

| File | Encoding | Delimiter | Date Format | Rows |
|------|----------|-----------|------------|------|
| file.csv | UTF-8 | ; | DD/MM/YYYY | N |

## Columns

| Column | Type | Nullable | Sample |
|--------|------|----------|--------|
| id | string | no | 12345 |

## Cleaning Rules

- Remove control chars
- Parse dates as DD/MM/YYYY
- Trim whitespace
```

## Return Format

Return to the orchestrator:
- status: "complete" | "blocked"
- executive_summary: encoding, delimiter, date format detected
- artifacts: ["estudios/<project>/esquema.md"]
- next_recommended: "data-sql" or "data-etl"

## Artifact Store

Save progress to engram: `data/{project}/study-progress`
