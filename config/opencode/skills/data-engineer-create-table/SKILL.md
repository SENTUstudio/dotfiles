---
name: data-engineer-create-table
description: >
  Guides the three-phase workflow for creating new Glue tables: ETL schema extraction, INFRA table definition, and enable write.
  Trigger: When creating new Glue table with three-phase workflow.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- When a new ETL source needs a corresponding Glue table
- When creating refined zone tables from raw S3 landing
- When transitioning from schema extraction to production
- During `sdd-spec` (Phase 1) and `sdd-apply` (Phase 2-3) phases

## Critical Patterns

### Three-Phase Workflow

```
Phase 1 (CARGA repo): ETL schema extraction
├── Build ETL script with source → df_final
├── Comment out write sections
├── Run in dev → df_final.printSchema()
├── Document: [(column_name, type), ...]
└── Output: Column list with types

Phase 2 (INFRA repo): Table definition
├── Create glue-tables/<name>.yaml
├── Add AWS::Glue::Table to template.yaml
├── Deploy: aws cloudformation deploy
└── Output: Table exists in Glue Catalog

Phase 3 (CARGA repo): Enable writes
├── Uncomment S3 write block
├── Uncomment catalog sync (wr.athena.repair_table)
├── Commit ETL, deploy CARGA stack
└── Output: ETL writes to table
```

### YAML Table Definition Structure

```yaml
Name:
          'Fn::Sub': 'stg_encuestas${DBDiscriminator}'
Description: !Sub "Stage ${AWS::StackName} <table description>"
TableType: EXTERNAL_TABLE
Parameters:
  classification: parquet
  compressionType: snappy
  parquet.compression: SNAPPY
StorageDescriptor:
  Columns:
    - Name: "col1"
      Type: "string"
    - Name: "col2"
      Type: "int"
    - Name: "col3"
      Type: "decimal(18,2)"
  Location:
    'Fn::Sub': 's3://${BucketName}/<prefix>/'
  InputFormat: org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat
  OutputFormat: org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat
  SerdeInfo:
    SerializationLibrary: org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe
  PartitionKeys:
    - Name: "year"
      Type: "string"
    - Name: "month"
      Type: "string"
    - Name: "day"
      Type: "string"
```

### Glue Data Type Mapping

| Python/Spark Type | Glue/Hive Type |
|-------------------|----------------|
| `string` | `string` |
| `int` | `int` |
| `long` | `bigint` |
| `float` | `float` |
| `double` | `double` |
| `decimal(18,2)` | `decimal(18,2)` |
| `timestamp` | `timestamp` |
| `date` | `date` |
| `boolean` | `boolean` |
| `array<string>` | `array<string>` |
| `map<string,string>` | `map<string,string>` |

## Code Examples

### Phase 1: ETL Schema Extraction

```python
# In CARGA repo: ETL script with commented writes

# Read source data
df = spark.read.csv(s3_files, header=True, sep=";", encoding="latin-1")

# Transform
df_final = df.select(
    col("id").cast("string"),
    col("fecha").cast("timestamp"),
    col("monto").cast("decimal(18,2)"),
    col("region").cast("string")
)

# Add partition columns
df_final = df_final.withColumn("year", lit(today.strftime("%Y")))
df_final = df_final.withColumn("month", lit(today.strftime("%m")))
df_final = df_final.withColumn("day", lit(today.strftime("%d")))

# COMMENTED FOR SCHEMA EXTRACTION
# df_final.write.mode("append").partitionBy("year", "month", "day").parquet(S3_OUTPUT_PATH)
# wr.athena.repair_table(table=GLUE_TABLE, database=GLUE_DATABASE)

# SCHEMA OUTPUT
df_final.printSchema()
```

### Phase 2: INFRA Table YAML

```yaml
# File: infra-datos-<project>/glue-tables/stg_<table_name>.yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "Glue table definition for <table_name>"

Resources:
  StgTableName:
    Type: AWS::Glue::Table
    Properties:
      CatalogId: !Ref AWS::AccountId
      DatabaseName: !Ref DatabaseName
      TableInput:
        Name:
          Fn::Sub: 'stg_encuestas${DBDiscriminator}'
        Description: !Sub "Stage ${AWS::StackName} <description>"
        TableType: EXTERNAL_TABLE
        Parameters:
          classification: parquet
          compressionType: snappy
          parquet.compression: SNAPPY
        StorageDescriptor:
          Columns:
            - Name: "id"
              Type: "string"
            - Name: "fecha"
              Type: "timestamp"
            - Name: "monto"
              Type: "decimal(18,2)"
            - Name: "region"
              Type: "string"
          Location:
            Fn::Sub: 's3://${BucketName}/<prefix>/'
          InputFormat: org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat
          OutputFormat: org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat
          SerdeInfo:
            SerializationLibrary: org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe
            SerdeParameters:
              serialization.format: "1"
          PartitionKeys:
            - Name: "year"
              Type: "string"
            - Name: "month"
              Type: "string"
            - Name: "day"
              Type: "string"
```

### Phase 3: Enable Writes

```python
# Uncomment in CARGA repo ETL script:

# WRITE TO S3
df_final.write.mode("append").partitionBy("year", "month", "day").parquet(S3_OUTPUT_PATH)

# SYNC GLUE CATALOG
import awswrangler as wr
wr.athena.repair_table(table=GLUE_TABLE, database=GLUE_DATABASE)
```

## Commands

### Phase 1: Run Schema Extraction

```bash
# In CARGA repo
cd estudios/<project>/
python -m glue_etl  # Outputs printSchema
```

### Phase 2: Deploy INFRA Stack

```bash
# In INFRA repo
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name infra-<table-name> \
    --parameter-overrides Environment=dev

# Verify table created
aws glue get-table --database-name toyota_chile_dev --table-name stg_table_name
```

### Phase 3: Deploy CARGA Stack

```bash
# In CARGA repo
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name carga-<table-name> \
    --parameter-overrides Environment=dev

# Run ETL
python -m glue_etl

# Verify data
aws athena query --query "SELECT COUNT(*) FROM toyota_chile_dev.stg_table_name"
```

## Output

The skill produces:
- **Phase 1**: ETL script with commented writes + column schema list
- **Phase 2**: `glue-tables/<name>.yaml` + template.yaml update
- **Phase 3**: ETL script with writes enabled + deployed stack

## Resources

- **Reference SAM templates**: See `toyota-chile-etl-template/migracion/PAP/infra-datos-stg-encuestas/`
- **Toyota Chile ETL Template**: See external `toyota-chile-etl-template/` artifact for project context