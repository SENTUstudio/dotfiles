---
name: data-engineer-study-file
description: >
  Analyzes ETL source files (CSV, Excel) to determine encoding, delimiters, date formats, and cleaning rules.
  Trigger: When analyzing ETL source files for encoding, delimiters, or date formats.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- When a new ETL project starts and source files need to be understood
- When debugging encoding issues in existing ETL pipelines
- When detecting delimiter changes in source file exports
- When date format ambiguities cause ETL failures (day-first vs month-first)
- When character cleaning issues arise (BOM markers, control characters, unicode anomalies)

## Critical Patterns

### Encoding Detection Order
1. **UTF-8 first** — most common, check for BOM (`\ufeff`)
2. **Latin-1 / ISO-8859-1** — common for Spanish text (á, ñ, ü); same encoding but Latin-1 has looser validation
3. **Windows-1252** — fallback for Western European text with characters like smart quotes
4. **Auto-detect with chardet** — when manual inspection is inconclusive

### Delimiter Detection
- Sample first **10 rows** of the file
- Count occurrences of: comma `,`, semicolon `;`, pipe `|`, tab `\t`
- Whitespace delimiter is rarely used in Toyota Chile files
- **Toyota Chile files typically use `;` (semicolon)** as delimiter

### Date Format Detection
- Sample **50+ values** to identify locale patterns
- Common Toyota Chile formats:
  - `DD/MM/YYYY` — Spanish locale (day-first)
  - `MM/DD/YYYY` — US locale (month-first)
  - `YYYY-MM-DD` — ISO8601 (unambiguous)
- When date format is ambiguous (neither first nor second component exceeds 12), assume DD/MM/YYYY (Spanish locale for Toyota Chile) unless overridden by analyst
- Null representations: empty string, `NULL`, `N/A`, `"1900-01-01"` (Excel epoch)

### Control Character Removal
```
Remove: 0x00-0x1F (ASCII control characters)
EXCEPT: 0x09 (tab), 0x0A (newline), 0x0D (carriage return)
```

### Unicode Anomaly Detection
- `Ã¡` → `á` indicates **ISO-8859-1 bytes interpreted as UTF-8**
- `Ã±` → `ñ` pattern confirms double-encoding
- `â€"` → `"` indicates Windows-1252 → UTF-8 double encoding

## Code Examples

### Python: Encoding Detection

```python
import chardet

def detect_encoding(file_path: str) -> dict:
    """Detect file encoding with confidence."""
    with open(file_path, 'rb') as f:
        raw = f.read(10000)  # Sample first 10KB
    result = chardet.detect(raw)
    return {
        'encoding': result['encoding'],
        'confidence': result['confidence'],
        'is_bom': raw.startswith(b'\xef\xbb\xbf')
    }
```

### Python: Delimiter Detection

```python
def detect_delimiter(file_path: str, encoding: str = 'utf-8') -> str:
    """Detect delimiter by counting occurrences in first 10 rows."""
    delimiters = {',': 0, ';': 0, '|': 0, '\t': 0}
    with open(file_path, 'r', encoding=encoding) as f:
        for i, line in enumerate(f):
            if i >= 10:
                break
            for d in delimiters:
                delimiters[d] += line.count(d)
    return max(delimiters, key=delimiters.get)
```

### Python: Date Format Detection

```python
from datetime import datetime
import re

DATE_PATTERNS = [
    (r'\d{4}-\d{2}-\d{2}', 'YYYY-MM-DD'),        # ISO8601 (unambiguous)
    (r'\d{2}/\d{2}/\d{4}', None),                 # Ambiguous — resolve with heuristic
]

def detect_date_format(sample_values: list) -> str:
    """Detect date format from sample values, disambiguating day-first vs month-first."""
    formats = {}
    for val in sample_values:
        v = str(val)
        for pattern, fmt in DATE_PATTERNS:
            if re.match(pattern, v):
                if fmt is None:
                    first, second = int(v.split('/')[0]), int(v.split('/')[1])
                    if first > 12:
                        fmt = 'DD/MM/YYYY'
                    elif second > 12:
                        fmt = 'MM/DD/YYYY'
                    else:
                        fmt = 'DD/MM/YYYY (ambiguous)'
                formats[fmt] = formats.get(fmt, 0) + 1
    return max(formats, key=formats.get) if formats else 'unknown'
```

### Python: Character Cleaning

```python
import re

CONTROL_CHARS = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')
LEADING_BOM = re.compile(r'^\ufeff')
DOUBLE_ENCODED = re.compile(r'Ã¡|Ã©|Ã­|Ã³|Ãº|Ã±|Ã')

def clean_value(value: str) -> str:
    """Clean control characters and BOM from string value."""
    if not isinstance(value, str):
        return value
    value = LEADING_BOM.sub('', value)  # Remove BOM
    value = CONTROL_CHARS.sub('', value)  # Remove control chars
    return value

def detect_double_encoding(sample: str) -> bool:
    """Detect ISO-8859-1 bytes interpreted as UTF-8."""
    return bool(DOUBLE_ENCODED.search(sample))
```

### Pandas: Reading with Detected Parameters

```python
import pandas as pd

def read_csv_with_detected_params(file_path: str, encoding: str, delimiter: str) -> pd.DataFrame:
    """Read CSV with pre-detected encoding and delimiter."""
    return pd.read_csv(
        file_path,
        encoding=encoding,
        sep=delimiter,
        header=0,  # Assume first row is header
        dtype=str,  # Read all as strings initially
        na_values=['', 'NULL', 'N/A', 'NA', 'none'],
        keep_default_na=False
    )
```

## Commands

### Quick File Inspection

```bash
# Check file encoding (hex dump)
head -c 100 file.csv | xxd | head -5

# Count lines
wc -l file.csv

# Check for BOM
head -c 3 file.csv | od -c

# Sample first 10 rows with visible delimiters
head -10 file.csv | cat -A
```

### Python: Full Analysis Script

```python
# study_file.py — Run this to analyze a source file
import sys
import pandas as pd

def analyze_file(file_path: str) -> dict:
    encoding_info = detect_encoding(file_path)
    delimiter = detect_delimiter(file_path, encoding_info['encoding'])
    
    df = pd.read_csv(file_path, encoding=encoding_info['encoding'], sep=delimiter, nrows=100)
    
    return {
        'file': file_path,
        'encoding': encoding_info,
        'delimiter': delimiter,
        'rows': len(df),
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'date_columns': [col for col in df.columns if 'date' in col.lower()]
    }

if __name__ == '__main__':
    result = analyze_file(sys.argv[1])
    import json; print(json.dumps(result, indent=2, default=str))
```

## Output

The analysis produces a **File Analysis Report** with:
- **File type**: CSV, Excel, or other
- **Encoding detected**: UTF-8/Latin-1/ISO-8859-1 with confidence
- **Delimiter identified**: comma/semicolon/pipe/tab
- **Date format patterns**: locale-ambiguous formats flagged
- **Cleaning rules**: bullet points for control chars, BOM, unicode anomalies
- **Sample values**: 5-10 example values per column for validation

## Resources

- **Toyota Chile ETL Template**: See external `toyota-chile-etl-template/` artifact for project context