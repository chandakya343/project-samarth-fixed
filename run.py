#!/usr/bin/env python3
"""
Project Samarth - Launch Script
Quick start script for the agricultural Q&A system
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['pandas', 'openpyxl', 'streamlit']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def main():
    """Main launch function"""
    print("🌾 PROJECT SAMARTH - Agricultural Q&A System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ Dependencies check passed")
    
    # Show options
    print("\n🚀 Choose an option:")
    print("1. Run demo (quick test)")
    print("2. Run full test suite")
    print("3. Launch web interface")
    print("4. Show project info")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🔄 Running demo...")
        subprocess.run([sys.executable, "demo.py"])
    
    elif choice == "2":
        print("\n🔄 Running full test suite...")
        subprocess.run([sys.executable, "test_system.py"])
    
    elif choice == "3":
        print("\n🌐 Launching web interface...")
        print("The app will open in your browser at http://localhost:8501")
        subprocess.run(["streamlit", "run", "app.py"])
    
    elif choice == "4":
        print("\n📋 PROJECT SAMARTH INFO")
        print("-" * 30)
        print("🎯 Purpose: Intelligent Q&A system for Indian agricultural data")
        print("📊 Data: 11,330+ records across 6 government datasets")
        print("🔧 Tech: Python, Pandas, Streamlit, OpenAI GPT")
        print("🎨 Design: Swiss aesthetic interface")
        print("\n📁 Key Files:")
        print("  • app.py - Web interface")
        print("  • qa_system.py - Main Q&A engine")
        print("  • data_loader.py - Data management")
        print("  • query_generator.py - LLM query generation")
        print("\n🚀 Quick Start:")
        print("  python3 demo.py          # Quick demo")
        print("  streamlit run app.py     # Web interface")
        print("  python3 test_system.py   # Full testing")
    
    else:
        print("❌ Invalid choice. Please run again.")

if __name__ == "__main__":
    main()

