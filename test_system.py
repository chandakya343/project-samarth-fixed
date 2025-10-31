#!/usr/bin/env python3
"""
Test script for Project Samarth
Tests the Q&A system with sample questions
"""

from qa_system import AgriculturalQASystem

def test_qa_system():
    """Test the Q&A system with sample questions"""
    print("🌾 Project Samarth - Agricultural Q&A System Test")
    print("=" * 60)
    
    # Initialize the system
    qa_system = AgriculturalQASystem()
    
    # Test questions
    test_questions = [
        "How many mandis are there in Punjab?",
        "What are the neighboring districts of Delhi?", 
        "List the top 5 crops available in the Agmark system",
        "Show me all districts in Maharashtra",
        "Which states have the most agricultural markets?"
    ]
    
    print("📊 Available Datasets:")
    datasets = qa_system.get_available_datasets()
    for name, info in datasets.items():
        print(f"  • {name}: {info['shape']} - {info['description']}")
    
    print(f"\n🔍 Testing {len(test_questions)} sample questions...")
    print("=" * 60)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 40)
        
        try:
            result = qa_system.ask_question(question)
            
            if result['success']:
                print(f"✅ Answer: {result['answer'][:200]}...")
                print(f"📚 Sources: {', '.join(result['sources'])}")
                
                # Show sample data
                if isinstance(result['raw_data'], list) and len(result['raw_data']) > 0:
                    print(f"📈 Sample Data: {len(result['raw_data'])} records found")
                elif isinstance(result['raw_data'], dict):
                    total_records = sum(len(v.get('data', [])) if isinstance(v, dict) else 0 for v in result['raw_data'].values())
                    print(f"📈 Sample Data: {total_records} total records across datasets")
            else:
                print(f"❌ Error: {result['answer']}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("-" * 40)
    
    print("\n🎉 Test completed!")
    print("\nTo run the web interface:")
    print("  streamlit run app.py")

if __name__ == "__main__":
    test_qa_system()

