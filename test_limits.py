#!/usr/bin/env python3
"""
Test the limits of Project Samarth with challenging queries
"""

import os
from dotenv import load_dotenv
from pipeline import SamarthPipeline

load_dotenv()

def test_limits():
    print("=" * 70)
    print("TESTING PROJECT SAMARTH - SYSTEM LIMITS")
    print("=" * 70)
    print()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found")
        return
    
    print("Initializing pipeline...")
    pipeline = SamarthPipeline(api_key)
    print("✓ Ready\n")
    
    # 5 challenging test queries
    test_queries = [
        # 1. Aggregation + Comparison
        "Which state has more mandis: Gujarat or Maharashtra?",
        
        # 2. Cross-dataset correlation
        "Which districts in Punjab have both mandis and IMD weather coverage?",
        
        # 3. Top-N with grouping
        "Show me the top 3 districts in each state by number of mandis",
        
        # 4. Multilingual data access
        "What are the Hindi names of crops that are vegetables?",
        
        # 5. Complex filtering + counting
        "How many districts have more than 20 mandis?"
    ]
    
    results = []
    
    for i, question in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/5: {question}")
        print('='*70)
        
        try:
            result = pipeline.process_question(question)
            
            if result['success']:
                print(f"\n✅ SUCCESS")
                print(f"\nAnswer: {result['answer'][:200]}...")
                print(f"\nSources: {len(result['citations'])} dataset(s)")
                results.append({'query': question, 'status': 'SUCCESS'})
            else:
                print(f"\n❌ FAILED: {result['error']}")
                results.append({'query': question, 'status': 'FAILED', 'error': result['error']})
                
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)[:100]}...")
            results.append({'query': question, 'status': 'ERROR', 'error': str(e)[:100]})
    
    # Summary
    print(f"\n\n{'='*70}")
    print("SUMMARY")
    print('='*70)
    
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    print(f"\nPassed: {success_count}/5")
    print(f"Failed: {5 - success_count}/5")
    
    for i, r in enumerate(results, 1):
        status_icon = "✅" if r['status'] == 'SUCCESS' else "❌"
        print(f"{status_icon} Test {i}: {r['status']}")
    
    print(f"\n{'='*70}")

if __name__ == "__main__":
    test_limits()

