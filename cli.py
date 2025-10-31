#!/usr/bin/env python3
"""
CLI Tool for Project Samarth
Simple command-line interface for the Q&A system
"""

import sys
import os
from pipeline import SamarthPipeline

def main():
    print("=" * 60)
    print("PROJECT SAMARTH - Agricultural Q&A System")
    print("=" * 60)
    print()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        print("Please set it with: export GEMINI_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Initialize pipeline
    print("Initializing pipeline...")
    try:
        pipeline = SamarthPipeline(api_key)
        print("✓ Pipeline initialized")
        print()
    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        sys.exit(1)
    
    # Interactive mode
    print("Enter your questions (type 'exit' to quit)")
    print("-" * 60)
    print()
    
    while True:
        try:
            question = input("Question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            print()
            print("Processing...")
            print("-" * 60)
            
            # Process question
            result = pipeline.process_question(question)
            
            print()
            print("=" * 60)
            
            if result['success']:
                print("ANSWER:")
                print(result['answer'])
                print()
                print("CITATIONS:")
                for citation in result['citations']:
                    print(f"  • {citation['name']}")
                    print(f"    Source: {citation['source']}")
            else:
                print("ERROR:")
                print(result['error'])
            
            print("=" * 60)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print()

if __name__ == "__main__":
    main()

