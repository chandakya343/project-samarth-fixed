# Project Samarth - README

## Overview
Project Samarth is an intelligent Q&A system for Indian agricultural and climate data, built for the Government Data Challenge. The system uses LLM-generated pandas queries to answer complex questions about agricultural markets, crops, locations, and climate patterns.

## Architecture
1. **Data Loader**: Loads and preprocesses agricultural datasets from bolbhav-data repository
2. **Query Generator**: Uses LLM to generate pandas DataFrame queries from natural language
3. **Q&A System**: Executes queries and formats responses with source citations
4. **Web Interface**: Streamlit-based frontend with Swiss design aesthetic

## Data Sources
- Agmark Mandis and Locations (4,053 mandis)
- Location Hierarchy (5,285 locations)
- District Neighbour Map (592 districts)
- APMC Mandi Map
- Agmark Crops (321 crops)
- IMD Agromet Advisory Locations (700 locations)

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
streamlit run app.py
```

## Features
- Natural language question processing
- Automatic query generation using LLM
- Source citation for all answers
- Real-time data processing
- Clean, modern interface

## Sample Questions
- "How many mandis are there in Punjab?"
- "What are the neighboring districts of Delhi?"
- "List the top 5 crops available in the Agmark system"
- "Show me all districts in Maharashtra"

