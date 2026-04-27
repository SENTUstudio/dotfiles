# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

See `_shared/skill-resolver.md` for the full resolution protocol.

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| When orchestrating complete Toyota Chile ETL project. | data-engineer-integrate | /Users/elepistemedev/.config/opencode/skills/data-engineer-integrate/SKILL.md |
| When creating new Glue table with three-phase workflow. | data-engineer-create-table | /Users/elepistemedev/.config/opencode/skills/data-engineer-create-table/SKILL.md |
| When building ETL pipeline from SharePoint source. | data-engineer-etl-sharepoint | /Users/elepistemedev/.config/opencode/skills/data-engineer-etl-sharepoint/SKILL.md |
| When building ETL pipeline from existing Glue Catalog table. | data-engineer-etl-glue | /Users/elepistemedev/.config/opencode/skills/data-engineer-etl-glue/SKILL.md |
| When building ETL pipeline from S3 source. | data-engineer-etl-s3 | /Users/elepistemedev/.config/opencode/skills/data-engineer-etl-s3/SKILL.md |
| When generating SQL for ETL transformations without provided SQL file. | data-engineer-sql-from-logic | /Users/elepistemedev/.config/opencode/skills/data-engineer-sql-from-logic/SKILL.md |
| When analyzing ETL source files for encoding, delimiters, or date formats. | data-engineer-study-file | /Users/elepistemedev/.config/opencode/skills/data-engineer-study-file/SKILL.md |
| When writing Go tests, using teatest, or adding test coverage. | go-testing | /Users/elepistemedev/.config/opencode/skills/go-testing/SKILL.md |
| When creating a GitHub issue, reporting a bug, or requesting a feature. | issue-creation | /Users/elepistemedev/.config/opencode/skills/issue-creation/SKILL.md |
| When user asks to create a new skill, add agent instructions, or document patterns for AI. | skill-creator | /Users/elepistemedev/.config/opencode/skills/skill-creator/SKILL.md |
| When creating a pull request, opening a PR, or preparing changes for review. | branch-pr | /Users/elepistemedev/.config/opencode/skills/branch-pr/SKILL.md |
| When user says "judgment day", "judgment-day", "review adversarial", "dual review", "doble review", "juzgar", "que lo juzguen". | judgment-day | /Users/elepistemedev/.config/opencode/skills/judgment-day/SKILL.md |

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### data-engineer-integrate
- Lifecycle: PROJECT SETUP → SOURCE ANALYSIS → SQL GENERATION → ETL SELECTION → TABLE CREATION → QUALITY CHECKS
- Project structure in estudios/<project_name>/ with config/dev.yaml, config/prd.yaml, src/artefactos/
- Invoke sub-skills in order: study-file → sql-from-logic → etl-* → create-table

### data-engineer-create-table
- Three-phase workflow: Phase 1 ETL schema extraction → Phase 2 INFRA table definition → Phase 3 Enable writes
- Phase 1: Build ETL, comment out writes, run in dev, document column list
- Phase 2: Create glue-tables/<name>.yaml, add AWS::Glue::Table to template.yaml, deploy with CloudFormation
- Phase 3: Uncomment S3 write block and catalog sync, deploy CARGA stack
- Table Name format: 'Fn::Sub': 'stg_encuestas${DBDiscriminator}'

### data-engineer-etl-sharepoint
- Use msal.ConfidentialClientApplication for service-principal auth
- Required env vars: TENANT_ID, CLIENT_ID, CLIENT_SECRET
- SCOPE: https://graph.microsoft.com/.default
- Lambda-compatible: single handler function, lightweight deps
- Output: write to S3 as parquet

### data-engineer-etl-glue
- Read from Glue Catalog using create_dynamic_frame.from_catalog()
- Convert to DF and create temp views for SQL transformations
- Use Spark SQL (not Presto/PostgreSQL) — CAST(col AS INT), date_format(), NVL()/COALESCE()
- Multi-table pattern: loop CATALOG_TABLES list, create temp views, then run final SQL CTE

### data-engineer-etl-s3
- Incremental watermark pattern: metadata table with last_load_timestamp
- Required metadata DDL: CREATE EXTERNAL TABLE {database}.{table}_metadata (last_load_timestamp TIMESTAMP)
- Partition output by year/month/day: .partitionBy("year", "month", "day").parquet(S3_OUTPUT_PATH)
- If metadata table missing, fallback to epoch (1970-01-01) and process all files

### data-engineer-sql-from-logic
- CTE naming: filtered_data, enriched_with_*, deduplicated, aggregated_*, windowed_*, final_output
- Spark SQL compatibility: CAST not ::, date_format not TO_CHAR, NVL/COALESCE for nulls
- Date ambiguity: assume DD/MM/YYYY (Spanish locale) unless overridden
- Output to src/artefactos/<table_name>.sql (staging area, not in official repos)
- Every SQL file MUST have header comment block with table name, source, author, date

### data-engineer-study-file
- Encoding detection order: UTF-8 (check BOM) → Latin-1/ISO-8859-1 → Windows-1252 → chardet auto-detect
- Delimiter: sample 10 rows, count comma/semicolon/pipe/tab; Toyota Chile typically uses semicolon
- Date format: sample 50+ values; assume DD/MM/YYYY when ambiguous
- Control chars: remove 0x00-0x1F except 0x09 (tab), 0x0A (newline), 0x0D (CR)
- Unicode anomaly: Ã¡ → á indicates ISO-8859-1 bytes read as UTF-8

### go-testing
- Table-driven tests are standard: tests := []struct{name, input, expected, wantErr}
- Use teatest for Bubbletea TUI testing
- Golden file testing: compare output against committed .golden files
- Integration tests: use httptest for HTTP handlers
- Coverage: go test -cover or go test -coverprofile=coverage.out

### issue-creation
- Blank issues are disabled — MUST use template (bug report or feature request)
- Every issue gets status:needs-review automatically
- Maintainer MUST add status:approved before any PR can be opened
- Questions go to Discussions, not issues
- Search existing issues for duplicates before creating

### skill-creator
- Skill structure: skills/{skill-name}/SKILL.md, optional assets/, optional references/
- Frontmatter required: name, description (with Trigger:), license, metadata (author, version)
- Create skill only for repeated patterns, complex workflows, or project-specific conventions
- Don't create for trivial one-off tasks or existing documentation
- Use allowed-tools in frontmatter if skill needs specific tools

### branch-pr
- Every PR MUST link an approved issue — no exceptions
- Every PR MUST have exactly one type:* label
- Blank PRs without issue linkage are blocked by GitHub Actions
- Branch naming regex: ^(feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert)\/[a-z0-9._-]+$
- Run shellcheck on modified scripts before PR

### judgment-day
- BEFORE launching judges: resolve skills via registry, build Project Standards block, inject into all prompts
- Launch TWO sub-agents via delegate in PARALLEL — never sequential
- Judges are BLIND — neither knows about the other
- Synthesize verdicts: merge findings, deduplicate, severity rank
- Fix Agent applies changes, then re-judge (max 2 iterations)
- If still failing after 2 iterations, escalate to user

## Project Conventions

| File | Path | Notes |
|------|------|-------|
| No convention files found | — | No agents.md, AGENTS.md, CLAUDE.md, .cursorrules, GEMINI.md, or copilot-instructions.md detected in project root |

Read the convention files listed above for project-specific patterns and rules. All referenced paths have been extracted — no need to read index files to discover more.
