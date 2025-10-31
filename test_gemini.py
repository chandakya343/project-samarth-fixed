#!/usr/bin/env python3
"""
Quick test of the Gemini-based system
"""

import os
from dotenv import load_dotenv
from pipeline import SamarthPipeline

# Load environment variables
load_dotenv()

def test_system():
    print("=" * 60)
    print("TESTING PROJECT SAMARTH - GEMINI SYSTEM")
    print("=" * 60)
    print()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        return
    
    print(f"✓ API key loaded (length: {len(api_key)})")
    print()
    
    # Initialize pipeline
    print("Initializing pipeline...")
    try:
        pipeline = SamarthPipeline(api_key)
        print("✓ Pipeline initialized successfully")
        print()
    except Exception as e:
        print(f"❌ Error initializing pipeline: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test question
    test_question = "How many mandis are there in Punjab?"
    print(f"Test Question: {test_question}")
    print("-" * 60)
    print()
    
    try:
        result = pipeline.process_question(test_question)
        
        print()
        print("=" * 60)
        print("RESULT:")
        print("=" * 60)
        
        if result['success']:
            print(f"\n✅ Success!\n")
            print("ANSWER:")
            print(result['answer'])
            print()
            print("CITATIONS:")
            for citation in result['citations']:
                print(f"  • {citation['name']}")
                print(f"    Source: {citation['source']}")
            print()
            print(f"Trace saved: Check llm_logs/ directory")
        else:
            print(f"\n❌ Error: {result['error']}")
        
    except Exception as e:
        print(f"\n❌ Error processing question: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_system()

