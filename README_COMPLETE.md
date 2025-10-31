# Project Samarth - Complete System

## 🎯 Overview

An intelligent Q&A system for Indian agricultural and climate data, built with Gemini 2.5 Flash. The system uses a 2-LLM pipeline to understand questions, generate pandas queries, and provide grounded answers with source citations.

---

## 🚀 Quick Start

### Launch Web Interface (Recommended)

```bash
# Option 1: Use launch script
./launch.sh

# Option 2: Direct command
streamlit run streamlit_app.py
```

Opens at: `http://localhost:8501`

### Launch CLI

```bash
python3 cli.py
```

---

## 📁 Project Structure

```
project_samarth/
├── streamlit_app.py          # Web interface ⭐
├── cli.py                     # Command-line interface
├── pipeline.py                # Main orchestrator
├── gemini_client.py           # Gemini API wrapper
├── schema_builder.py          # Dataset routing
├── query_generator_gemini.py  # LLM Call #1
├── executor.py                # Query execution
├── answer_synthesizer.py      # LLM Call #2
├── data_loader.py             # Data loading
├── data/                      # 6 datasets (11,330 records)
├── llm_logs/                  # All LLM inputs/outputs
├── test_gemini.py             # Basic test
├── test_limits.py             # 5 challenging queries
└── launch.sh                  # Quick launch script
```

---

## 🎨 Web Interface Features

### Main Panel
- **Question Input**: Large text area with examples
- **Answer Display**: Clean formatting with citations
- **Action Buttons**: Ask / Clear

### Sidebar
- **About**: System description
- **6 Dataset Cards**: 
  - Record counts
  - Descriptions  
  - Key fields
- **8 Sample Questions**: One-click examples
- **System Stats**: Total records, datasets, states

### Right Panel
- **Recent Questions**: Last 5 questions
- **Ask Again**: Re-run previous queries

---

## 📊 Available Datasets

| Dataset | Records | Description |
|---------|---------|-------------|
| Agmark Mandis | 4,062 | Agricultural markets across India |
| Location Hierarchy | 5,294 | State → District → Block structure |
| District Neighbours | 601 | Neighboring district mappings |
| APMC Mandis | 352 | APMC market data |
| Agmark Crops | 321 | Crop varieties (multilingual) |
| IMD Weather | 700 | Weather advisory locations |

**Total: 11,330 records across 6 datasets**

---

## 💡 Sample Questions

### Simple Queries
- "How many mandis are in Punjab?"
- "List all crops in the Agmark system"
- "What districts are in Maharashtra?"

### Comparison Queries
- "Which state has more mandis: Gujarat or Maharashtra?"
- "Compare mandi counts between states"

### Cross-Dataset Queries
- "Which districts have both mandis and IMD weather coverage?"
- "Show districts with mandis and their neighbors"

### Aggregation Queries
- "Show me the top 5 states by number of mandis"
- "How many districts have more than 20 mandis?"
- "Top 3 districts in each state by mandi count"

### Multilingual Queries
- "What are the Hindi names of vegetable crops?"
- "Show crop names in Marathi"

---

## 🏗️ System Architecture

```
User Question
    ↓
Schema Builder (deterministic)
    ↓
Query Generation LLM (Gemini Call #1)
    ↓
Query Executor (deterministic)
    ↓
Citation Builder (deterministic)
    ↓
Answer Synthesis LLM (Gemini Call #2)
    ↓
Final Answer + Citations
```

**2 LLM calls per question. Everything else is deterministic.**

---

## 🔍 Debugging & Logging

All LLM interactions logged to `llm_logs/`:

- `query_generation_*_INPUT_RAW.txt` - Prompt #1
- `query_generation_*_OUTPUT_RAW.txt` - Generated code
- `answer_synthesis_*_INPUT_RAW.txt` - Prompt #2
- `answer_synthesis_*_OUTPUT_RAW.txt` - Final answer
- `TRACE_*.json` - Complete execution trace

---

## ✅ Test Results

**5/5 challenging queries passed:**
1. ✅ Aggregation + Comparison
2. ✅ Cross-dataset correlation
3. ✅ Complex grouping (top N per group)
4. ✅ Multilingual data access
5. ✅ Complex filtering + counting

Run tests:
```bash
python3 test_gemini.py      # Basic test
python3 test_limits.py      # 5 challenging queries
```

---

## 📝 Key Files to Review

**The Two Prompts (Non-Deterministic):**
1. `query_generator_gemini.py` lines 40-65 - Query generation
2. `answer_synthesizer.py` lines 35-80 - Answer synthesis

**Everything else is deterministic code.**

---

## 🎬 Demo Flow

1. **Launch**: `./launch.sh` or `streamlit run streamlit_app.py`
2. **Show Interface**: Clean design, dataset info visible
3. **Click Sample**: "How many mandis in Punjab?" → 349 mandis
4. **Try Complex**: "Which state has more mandis?" → Gujarat > Maharashtra
5. **Show Cross-Dataset**: "Districts with mandis and weather coverage"
6. **Show Logs**: Open `llm_logs/` to show raw prompts
7. **Explain**: 2 LLM calls, deterministic execution, citations

---

## 🔧 Configuration

**Required:**
- `.env` file with `GEMINI_API_KEY` ✅ (already configured)
- Python 3.9+
- Dependencies: `pip install -r requirements.txt`

**Optional:**
- Customize prompts in `query_generator_gemini.py` and `answer_synthesizer.py`
- Adjust `max_results` in pipeline (default: 20)

---

## 📚 Documentation

- `QUICKSTART.md` - Quick start guide
- `FINAL_SUMMARY.md` - Complete implementation summary
- `INTERFACE_GUIDE.md` - UI layout and features
- `PROMPTS_LOCATION.md` - Where to find the prompts
- `SYSTEM_DIAGRAM.md` - Visual architecture
- `DATABASE_SCHEMA_EDA_REPORT.md` - Data analysis
- `WHAT_CAN_THIS_DATA_ANSWER.md` - Query examples

---

## 🏆 Achievement

Built exactly as specified:
- ✅ 2-LLM pipeline (Gemini 2.5 Flash)
- ✅ XML-structured prompts
- ✅ Full logging (every input/output)
- ✅ Deterministic citations
- ✅ Web interface with dataset info
- ✅ Sample questions for easy start
- ✅ 5/5 test queries passed
- ✅ Clean, professional design
- ✅ Ready for demo

**The system is production-ready!** 🎉
