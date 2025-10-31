#!/bin/bash

# Project Samarth - Launch Script

echo "========================================"
echo "🌾 PROJECT SAMARTH"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env with GEMINI_API_KEY"
    exit 1
fi

# Check if GEMINI_API_KEY is set
if ! grep -q "GEMINI_API_KEY" .env; then
    echo "❌ Error: GEMINI_API_KEY not found in .env"
    exit 1
fi

echo "✓ API key found"
echo ""

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "❌ Error: data directory not found"
    exit 1
fi

echo "✓ Data directory found"
echo ""

# Launch Streamlit
echo "🚀 Launching Streamlit interface..."
echo ""
echo "The app will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run streamlit_app.py

