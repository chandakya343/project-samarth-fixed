# Project Samarth - Quick Start Guide

## 🚀 Launch the System

### Option 1: Streamlit Web Interface (Recommended)

```bash
# Make sure you're in the project directory
cd /Users/aryanchandak/projects/project_samarth/project_samarth

# Run Streamlit app
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Option 2: Command Line Interface

```bash
# Run CLI
python3 cli.py
```

## 📋 Features

### Web Interface
- **Left Panel**: Main question input and answer display
- **Right Panel**: Recent questions history
- **Sidebar**: 
  - Dataset information (6 datasets with details)
  - Sample questions (8 pre-loaded examples)
  - System statistics

### What You Can Ask

#### Simple Queries
- "How many mandis are in Punjab?"
- "List all crops in the Agmark system"
- "What districts are in Maharashtra?"

#### Comparison Queries
- "Which state has more mandis: Gujarat or Maharashtra?"
- "Compare mandi counts between Punjab and Haryana"

#### Cross-Dataset Queries
- "Which districts in Punjab have both mandis and IMD weather coverage?"
- "Show districts with mandis and their neighboring districts"

#### Aggregation Queries
- "Show me the top 5 states by number of mandis"
- "How many districts have more than 20 mandis?"
- "What are the top 3 districts in each state by mandi count?"

#### Multilingual Queries
- "What are the Hindi names of vegetable crops?"
- "Show me crop names in Marathi"

## 📊 Available Datasets

1. **Agmark Mandis and Locations** (4,062 records)
   - Agricultural markets across India
   - Fields: Mandi Name, District, State

2. **Location Hierarchy** (5,294 records)
   - State → Division → District → Block
   - Complete administrative structure

3. **District Neighbour Map** (601 records)
   - Neighboring districts for each district
   - Spatial relationships

4. **APMC Mandi Map** (352 records)
   - APMC market mappings
   - Punjab-focused data

5. **Agmark Crops** (321 records)
   - Crop varieties and types
   - Multilingual: English, Hindi, Marathi

6. **IMD Weather Locations** (700 records)
   - Weather advisory coverage
   - IMD station codes

## 🎯 How It Works

1. **You ask a question** in natural language
2. **Gemini generates** pandas query code
3. **System executes** the query on local data
4. **Gemini synthesizes** a grounded answer
5. **Citations provided** for all data sources

## 🔍 Debugging

All LLM calls are logged in `llm_logs/` directory:
- `query_generation_*_INPUT_RAW.txt` - Prompt sent to Gemini
- `query_generation_*_OUTPUT_RAW.txt` - Generated pandas code
- `answer_synthesis_*_INPUT_RAW.txt` - Evidence + context
- `answer_synthesis_*_OUTPUT_RAW.txt` - Final answer
- `TRACE_*.json` - Complete execution trace

## 💡 Tips

- Use the **sample questions** in the sidebar to get started
- Check **dataset information** to understand what data is available
- **Recent questions** panel lets you re-run previous queries
- All answers include **source citations** for traceability

## 🎬 Ready for Demo

The system is fully functional and ready for your Loom video demonstration!
