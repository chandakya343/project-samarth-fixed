# System Architecture Diagram - Project Samarth

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER QUESTION                                │
│                    "How many mandis in Punjab?"                      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: Schema Builder (DETERMINISTIC)                             │
│  ────────────────────────────────────────────────────────────────   │
│  • Keyword matching: "mandi" → agmark_mandis_and_locations          │
│  • Build XML schema: columns, dtypes, 2-3 sample rows               │
│  • Output: <SCHEMA>...</SCHEMA>                                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2: Query Generation LLM (GEMINI CALL #1)                      │
│  ────────────────────────────────────────────────────────────────   │
│  Input Prompt (XML):                                                │
│    <SYSTEM>You are a data analyst...</SYSTEM>                       │
│    <SCHEMA>...relevant datasets only...</SCHEMA>                    │
│    <QUESTION>How many mandis in Punjab?</QUESTION>                  │
│    <CONSTRAINTS>Use exact names, cap to 20...</CONSTRAINTS>         │
│    <OUTPUT_FORMAT><PANDAS_CODE>...</PANDAS_CODE></OUTPUT_FORMAT>    │
│                                                                      │
│  Output:                                                             │
│    <PANDAS_CODE>                                                     │
│    mandis_df = data_loader.get_dataframe('agmark_mandis_...')       │
│    result = mandis_df[mandis_df['State Name']                       │
│             .str.contains('Punjab', case=False)].head(20)           │
│    </PANDAS_CODE>                                                    │
│                                                                      │
│  Logged to: llm_logs/query_generation_*_INPUT_RAW.txt               │
│             llm_logs/query_generation_*_OUTPUT_RAW.txt               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3: Query Executor (DETERMINISTIC)                             │
│  ────────────────────────────────────────────────────────────────   │
│  • Execute pandas code in sandboxed environment                     │
│  • Cap results to 20 rows                                           │
│  • Build evidence bundle:                                           │
│    {                                                                │
│      "type": "DataFrame",                                           │
│      "shape": [20, 6],                                              │
│      "columns": ["Mandi Name", "State Name", ...],                  │
│      "records": [{...}, {...}, ...],                                │
│      "summary_stats": {                                             │
│        "total_rows": 349,                                           │
│        "rows_returned": 20,                                         │
│        "capped": true                                               │
│      }                                                              │
│    }                                                                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 4: Citation Builder (DETERMINISTIC)                           │
│  ────────────────────────────────────────────────────────────────   │
│  • Extract dataset names from executed code                         │
│  • Map to source information:                                       │
│    [                                                                │
│      {                                                              │
│        "name": "Agmark Mandis and Locations Dataset",               │
│        "source": "Agmarknet (agmarknet.gov.in)",                    │
│        "description": "Agricultural markets across India"           │
│      }                                                              │
│    ]                                                                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 5: Answer Synthesis LLM (GEMINI CALL #2)                      │
│  ────────────────────────────────────────────────────────────────   │
│  Input Prompt (XML):                                                │
│    <SYSTEM>You are a precise analyst...</SYSTEM>                    │
│    <QUESTION>How many mandis in Punjab?</QUESTION>                  │
│    <EXECUTED_CODE>mandis_df = ...</EXECUTED_CODE>                   │
│    <EVIDENCE>{...evidence bundle JSON...}</EVIDENCE>                │
│    <CITATIONS>                                                       │
│      <SOURCE>                                                        │
│        <name>Agmark Mandis and Locations Dataset</name>             │
│        <source>Agmarknet (agmarknet.gov.in)</source>                │
│      </SOURCE>                                                       │
│    </CITATIONS>                                                      │
│    <INSTRUCTIONS>Use only evidence, cite numbers...</INSTRUCTIONS>  │
│    <OUTPUT_FORMAT>Answer + Sources:</OUTPUT_FORMAT>                 │
│                                                                      │
│  Output:                                                             │
│    "Punjab has 349 agricultural markets (mandis) across various     │
│     districts. Top districts: Sangrur (36), Jalandhar (36)...       │
│     (Showing top 20 from 349 total)                                 │
│                                                                      │
│     Sources:                                                         │
│     - Agmark Mandis and Locations Dataset"                          │
│                                                                      │
│  Logged to: llm_logs/answer_synthesis_*_INPUT_RAW.txt               │
│             llm_logs/answer_synthesis_*_OUTPUT_RAW.txt               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FINAL OUTPUT                                                        │
│  ────────────────────────────────────────────────────────────────   │
│  Answer: Punjab has 349 mandis...                                   │
│  Citations: Agmark Mandis and Locations Dataset                     │
│  Trace: llm_logs/TRACE_*.json                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Points

### LLM Calls (Non-Deterministic)
1. **Query Generation** (Gemini Call #1)
   - Input: Question + Schema XML
   - Output: Pandas code in `<PANDAS_CODE>` tags

2. **Answer Synthesis** (Gemini Call #2)
   - Input: Question + Code + Evidence JSON + Citations XML
   - Output: Grounded answer with sources

### Deterministic Steps
1. **Schema Builder**: Keyword routing + XML generation
2. **Executor**: Code execution + evidence building
3. **Citation Builder**: Dataset extraction + source mapping

### Logging
- Every LLM input/output saved in raw form
- Complete trace with timestamps
- Easy debugging via `llm_logs/` directory
