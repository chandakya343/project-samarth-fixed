# Prompt Locations - Project Samarth

## 🎯 The Two LLM Prompts (Non-Deterministic Parts)

### **Prompt #1: Query Generation**
**File**: `query_generator_gemini.py`  
**Method**: `_build_query_generation_prompt()`  
**Line**: ~40-65

**Structure**:
```xml
<SYSTEM>You are a senior data analyst who writes precise pandas queries.</SYSTEM>

<SCHEMA>
  <!-- Dynamically generated XML with relevant datasets only -->
  <DATASET name="...">
    <row_count>...</row_count>
    <columns>
      <column name="..." dtype="..." unique="..." nulls="..."/>
    </columns>
    <sample_rows>
      <row index="0">
        <field name="...">value</field>
      </row>
    </sample_rows>
  </DATASET>
</SCHEMA>

<QUESTION>
{user_question}
</QUESTION>

<CONSTRAINTS>
- Use exact dataframe names and column names as shown in <SCHEMA>
- Access dataframes using: data_loader.get_dataframe('dataset_name')
- Prefer boolean masking, groupby/agg, sort_values
- Always cap outputs with .head(20)
- Avoid joins unless necessary
- Handle null values appropriately
- Use .str.contains() with case=False for string matching
- Return a single code block that assigns final result to variable named 'result'
</CONSTRAINTS>

<OUTPUT_FORMAT>
Return only the pandas code inside <PANDAS_CODE> tags.
Example:
<PANDAS_CODE>
# Get mandis in Punjab
mandis_df = data_loader.get_dataframe('agmark_mandis_and_locations')
result = mandis_df[mandis_df['State Name'].str.contains('Punjab', case=False)].head(20)
</PANDAS_CODE>
</OUTPUT_FORMAT>
```

**What to tune**:
- `<SYSTEM>` role description
- `<CONSTRAINTS>` rules
- `<OUTPUT_FORMAT>` structure and examples

---

### **Prompt #2: Answer Synthesis**
**File**: `answer_synthesizer.py`  
**Method**: `_build_synthesis_prompt()`  
**Line**: ~35-80

**Structure**:
```xml
<SYSTEM>You are a precise policy/data analyst. Cite exact numbers and sources.</SYSTEM>

<QUESTION>
{user_question}
</QUESTION>

<EXECUTED_CODE>
{pandas_code_that_was_executed}
</EXECUTED_CODE>

<EVIDENCE>
{
  "type": "DataFrame",
  "shape": [20, 6],
  "columns": ["Mandi Name - Agmark", "State Name", ...],
  "records": [
    {"Mandi Name - Agmark": "...", "State Name": "..."},
    ...
  ],
  "summary_stats": {
    "total_rows": 349,
    "rows_returned": 20,
    "capped": true
  },
  "datasets_used": ["agmark_mandis_and_locations"]
}
</EVIDENCE>

<CITATIONS>
  <SOURCE>
    <name>Agmark Mandis and Locations Dataset</name>
    <source>Agmarknet (agmarknet.gov.in)</source>
    <description>Agricultural markets (mandis) across India</description>
  </SOURCE>
</CITATIONS>

<INSTRUCTIONS>
- Use only data from <EVIDENCE>; do not invent values
- Include explicit comparisons/trends if relevant
- Call out data gaps/limits (row caps, missing fields)
- Keep answer compact; use bullets where helpful
- Be specific with numbers and names from the evidence
- If evidence shows the data was capped, mention "showing top N results"
</INSTRUCTIONS>

<OUTPUT_FORMAT>
Provide a concise answer paragraph or bullets, then end with:

Sources:
- [List source names from <CITATIONS>]
</OUTPUT_FORMAT>
```

**What to tune**:
- `<SYSTEM>` role description
- `<INSTRUCTIONS>` reasoning guidelines
- `<OUTPUT_FORMAT>` answer structure

---

## 🔍 How to Debug

All LLM inputs and outputs are saved in `llm_logs/` directory:

### Log Files Created Per LLM Call:
- `query_generation_{timestamp}_INPUT.json` - Full input log with metadata
- `query_generation_{timestamp}_INPUT_RAW.txt` - Raw prompt text
- `query_generation_{timestamp}_OUTPUT.json` - Full output log with metadata
- `query_generation_{timestamp}_OUTPUT_RAW.txt` - Raw LLM response

- `answer_synthesis_{timestamp}_INPUT.json` - Full input log with metadata
- `answer_synthesis_{timestamp}_INPUT_RAW.txt` - Raw prompt text
- `answer_synthesis_{timestamp}_OUTPUT.json` - Full output log with metadata
- `answer_synthesis_{timestamp}_OUTPUT_RAW.txt` - Raw LLM response

### Complete Trace:
- `TRACE_{timestamp}.json` - Full pipeline execution trace with all steps

---

## 📊 Deterministic Parts (No Tuning Needed)

These are pure code - no LLM involved:

1. **Schema Builder** (`schema_builder.py`)
   - Keyword-based dataset routing
   - XML schema generation

2. **Query Executor** (`executor.py`)
   - Safe pandas code execution
   - Evidence bundle building
   - Citation extraction

3. **Pipeline Orchestrator** (`pipeline.py`)
   - Step sequencing
   - Trace logging

---

## 🚀 Usage

```bash
# Set API key
export GEMINI_API_KEY='your-key-here'

# Run CLI
python3 cli.py
```

---

## 📝 Quick Prompt Tuning Guide

To modify prompts:

1. **Query Generation**: Edit `query_generator_gemini.py` line ~40-65
   - Tune `<SYSTEM>` for better query understanding
   - Add/remove `<CONSTRAINTS>` for query quality
   - Modify `<OUTPUT_FORMAT>` examples

2. **Answer Synthesis**: Edit `answer_synthesizer.py` line ~35-80
   - Tune `<SYSTEM>` for answer style
   - Adjust `<INSTRUCTIONS>` for reasoning depth
   - Modify `<OUTPUT_FORMAT>` for citation style

3. **Test**: Run `python3 cli.py` and check `llm_logs/` for raw inputs/outputs

4. **Iterate**: Look at `*_RAW.txt` files to see exactly what Gemini saw and returned
