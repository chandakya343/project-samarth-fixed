# Project Samarth - New Gemini-Based System

## 🎯 Architecture

**2-LLM Call Pipeline with Full Logging**

```
User Question
    ↓
[1] Schema Builder (deterministic)
    → Identifies relevant datasets
    → Builds XML schema context
    ↓
[2] Query Generation LLM (Gemini Call #1)
    → Generates pandas query code
    → Outputs <PANDAS_CODE>...</PANDAS_CODE>
    ↓
[3] Query Executor (deterministic)
    → Executes pandas code safely
    → Builds evidence bundle (capped to 20 rows)
    ↓
[4] Citation Builder (deterministic)
    → Extracts datasets used
    → Maps to source information
    ↓
[5] Answer Synthesis LLM (Gemini Call #2)
    → Reasons over evidence
    → Generates grounded answer with citations
    ↓
Final Answer + Sources
```

## 📁 File Structure

```
project_samarth/
├── gemini_client.py          # Gemini API wrapper with logging
├── schema_builder.py          # Dataset routing + XML schema generation
├── query_generator_gemini.py # LLM Call #1: Query generation
├── executor.py                # Query execution + evidence building
├── answer_synthesizer.py     # LLM Call #2: Answer synthesis
├── pipeline.py                # Main orchestrator
├── cli.py                     # Command-line interface
├── data_loader.py             # Data loading (existing)
└── llm_logs/                  # All LLM inputs/outputs saved here
```

## 🚀 Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set API key**:
```bash
export GEMINI_API_KEY='your-gemini-api-key-here'
```

3. **Run CLI**:
```bash
python3 cli.py
```

## 📝 Example Session

```
Question: How many mandis are in Punjab?

Processing...
--------------------------------------------------
Step 1: Generating pandas query...
✓ Generated query (log: query_generation_2025-01-30T10-30-45)
Step 2: Executing query...
✓ Query executed successfully
Step 3: Building citations...
✓ Built 1 citations
Step 4: Synthesizing answer...
✓ Answer synthesized (log: answer_synthesis_2025-01-30T10-30-47)
✓ Trace saved: llm_logs/TRACE_2025-01-30T10-30-45.json

============================================================
ANSWER:
Punjab has 349 agricultural markets (mandis) across various districts. 
The top districts by mandi count are:
- Sangrur: 36 mandis
- Jalandhar: 36 mandis
- Bhatinda: 33 mandis
- Ludhiana: 31 mandis

(Showing top 20 results from total 349 records)

Sources:
  • Agmark Mandis and Locations Dataset
    Source: Agmarknet (agmarknet.gov.in)
============================================================
```

## 🔍 Debugging

All LLM calls are logged to `llm_logs/`:

- `query_generation_*_INPUT_RAW.txt` - Exact prompt sent to Gemini (Call #1)
- `query_generation_*_OUTPUT_RAW.txt` - Exact response from Gemini (Call #1)
- `answer_synthesis_*_INPUT_RAW.txt` - Exact prompt sent to Gemini (Call #2)
- `answer_synthesis_*_OUTPUT_RAW.txt` - Exact response from Gemini (Call #2)
- `TRACE_*.json` - Complete execution trace with all steps

## 📝 Prompt Locations

See `PROMPTS_LOCATION.md` for exact file/line numbers of the two LLM prompts.

**Quick Reference**:
- **Prompt #1**: `query_generator_gemini.py` line ~40-65
- **Prompt #2**: `answer_synthesizer.py` line ~35-80

## 🎯 Key Features

✅ **Exactly 2 LLM calls per question**  
✅ **XML-structured prompts** (Gemini-optimized)  
✅ **Full input/output logging** for debugging  
✅ **Deterministic citation** extraction  
✅ **Evidence capping** (max 20 rows)  
✅ **Safe code execution** (sandboxed)  
✅ **Complete trace** for every question  

## 🔧 No Fallbacks

This system requires a Gemini API key. There are no fallback modes - it's pure LLM-based query generation and synthesis.

## 📊 Data Coverage

- **4,062 mandis** across 36 states
- **321 crop varieties** with multilingual names
- **5,294 locations** (state/district/block hierarchy)
- **700 IMD weather stations**
- **601 district neighbor mappings**

## 🎬 Ready for Demo

The system logs everything needed for a Loom video:
1. User question
2. Generated pandas query
3. Execution results
4. Final answer with citations
5. Complete trace with timestamps
