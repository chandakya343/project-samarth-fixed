# Streamlit Interface Guide

## 🖥️ Interface Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     🌾 PROJECT SAMARTH                                   │
│        Intelligent Q&A System for Indian Agricultural & Climate Data    │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┬──────────────────────────────┬─────────────────────┐
│                  │                              │                     │
│   SIDEBAR        │     MAIN PANEL               │   RIGHT PANEL       │
│   (Left)         │     (Center)                 │   (Right)           │
│                  │                              │                     │
│ 🎯 About         │  🤔 Ask Your Question        │  💬 Recent          │
│ ────────────     │  ─────────────────────       │  Questions          │
│ System info      │                              │  ───────────        │
│                  │  [Large text input box]      │                     │
│ 📊 Available     │                              │  Q: How many...     │
│ Datasets         │  [🔍 Ask] [🗑️ Clear]        │  ↳ Answer: 349...   │
│ ────────────     │                              │  [Ask Again]        │
│                  │  📋 Answer                   │                     │
│ 📁 Agmark        │  ──────────                  │  Q: Which state...  │
│ Mandis (4,062)   │  ┌──────────────────────┐   │  ↳ Answer: Guj...   │
│ • Description    │  │ Gujarat has more      │   │  [Ask Again]        │
│ • Key fields     │  │ mandis than Maha...   │   │                     │
│                  │  └──────────────────────┘   │  Q: What crops...   │
│ 📁 Location      │                              │  ↳ Answer: Wheat... │
│ Hierarchy        │  📚 Data Sources             │  [Ask Again]        │
│ (5,294)          │  ────────────                │                     │
│ • Description    │  📄 Agmark Mandis Dataset    │                     │
│ • Key fields     │     Source: Agmarknet...     │                     │
│                  │                              │                     │
│ 📁 District      │                              │                     │
│ Neighbour Map    │                              │                     │
│ (601)            │                              │                     │
│                  │                              │                     │
│ 📁 APMC Mandi    │                              │                     │
│ Map (352)        │                              │                     │
│                  │                              │                     │
│ 📁 Agmark        │                              │                     │
│ Crops (321)      │                              │                     │
│                  │                              │                     │
│ 📁 IMD Weather   │                              │                     │
│ Locations (700)  │                              │                     │
│                  │                              │                     │
│ 💡 Sample        │                              │                     │
│ Questions        │                              │                     │
│ ────────────     │                              │                     │
│ 📌 How many      │                              │                     │
│ mandis in...     │                              │                     │
│                  │                              │                     │
│ 📌 Which state   │                              │                     │
│ has more...      │                              │                     │
│                  │                              │                     │
│ 📌 What          │                              │                     │
│ districts...     │                              │                     │
│                  │                              │                     │
│ 📈 System Stats  │                              │                     │
│ ────────────     │                              │                     │
│ Total: 11,330    │                              │                     │
│ Datasets: 6      │                              │                     │
│ States: 36       │                              │                     │
│                  │                              │                     │
└──────────────────┴──────────────────────────────┴─────────────────────┘
```

## 🎨 Key Features

### Sidebar (Left Panel)

**1. About Section**
- Brief system description
- What the system does

**2. Available Datasets (6 expandable cards)**
Each card shows:
- 📁 Dataset name
- Record count
- Description
- Key fields

Example:
```
📁 Agmark Mandis and Locations
Records: 4,062
Description: Agricultural markets (mandis) across India...
Key Fields: Mandi Name, District, State
```

**3. Sample Questions (8 clickable buttons)**
Pre-loaded questions like:
- 📌 How many mandis are in Punjab?
- 📌 Which state has more mandis: Gujarat or Maharashtra?
- 📌 What districts in Punjab have IMD weather coverage?
- etc.

**4. System Statistics**
- Total Records: 11,330
- Datasets: 6
- States Covered: 36

### Main Panel (Center)

**Question Input:**
- Large text area for typing questions
- Placeholder text with example
- Two buttons:
  - 🔍 Ask (primary action)
  - 🗑️ Clear (clear history)

**Answer Display:**
- Clean box with answer text
- Green left border for visual clarity
- Easy to read formatting

**Citations:**
- Each source in its own box
- Dataset name in bold
- Source information below

### Right Panel

**Recent Questions:**
- Shows last 5 questions
- Each in an expandable card
- Shows first 150 chars of answer
- "Ask Again" button to re-run

## 🎯 User Flow

1. **User arrives** → Sees clean interface with sample questions
2. **Clicks sample question** → Question auto-fills in input
3. **Clicks "Ask"** → System processes (shows spinner)
4. **Answer appears** → Clean formatted answer with citations
5. **Question saved** → Appears in "Recent Questions" panel
6. **User explores** → Can click other samples or type own question

## 💡 Design Principles

- **Swiss Design Aesthetic**: Clean, minimal, professional
- **Information Hierarchy**: Important info prominent
- **Easy Discovery**: Sample questions and dataset info visible
- **Quick Actions**: One-click sample questions
- **History**: Recent questions for reference
- **Citations**: Always show data sources

## 🎬 Demo Tips

1. **Start with sidebar** - Show dataset information
2. **Click a sample** - Instant question fill
3. **Show answer** - Clean formatting, citations
4. **Try complex query** - Show system capabilities
5. **Point to recent** - Show history feature
6. **Explain datasets** - Educational aspect

The interface is designed to be intuitive, educational, and professional!
