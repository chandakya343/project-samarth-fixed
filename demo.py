#!/usr/bin/env python3
"""
Project Samarth - Quick Demo Script
Demonstrates the key capabilities of the agricultural Q&A system
"""

from qa_system import AgriculturalQASystem
import json

def demo_system():
    """Quick demonstration of Project Samarth capabilities"""
    print("🌾 PROJECT SAMARTH - Agricultural Q&A System Demo")
    print("=" * 60)
    print("Built for the Government Data Challenge")
    print("Intelligent Q&A over Indian Agricultural & Climate Data")
    print("=" * 60)
    
    # Initialize system
    print("\n🔄 Initializing system...")
    qa_system = AgriculturalQASystem()
    
    # Show available data
    print("\n📊 Available Datasets:")
    datasets = qa_system.get_available_datasets()
    total_records = sum(info['shape'][0] for info in datasets.values())
    print(f"   Total Records: {total_records:,}")
    print(f"   Datasets: {len(datasets)}")
    
    # Demo questions
    demo_questions = [
        "How many mandis are there in Punjab?",
        "What are the neighboring districts of Delhi?",
        "List the top 5 crops available in the Agmark system"
    ]
    
    print(f"\n🔍 Demo Questions ({len(demo_questions)}):")
    print("-" * 40)
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n{i}. {question}")
        
        result = qa_system.ask_question(question)
        
        if result['success']:
            # Count records
            if isinstance(result['raw_data'], list):
                record_count = len(result['raw_data'])
            elif isinstance(result['raw_data'], dict):
                record_count = sum(len(v.get('data', [])) if isinstance(v, dict) else 0 for v in result['raw_data'].values())
            else:
                record_count = 1
            
            print(f"   ✅ Found {record_count} records")
            print(f"   📚 Sources: {', '.join(result['sources']) if result['sources'] else 'Multiple datasets'}")
            print(f"   💡 Answer: {result['answer'][:100]}...")
        else:
            print(f"   ❌ Error: {result['answer']}")
    
    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print("\n🚀 To run the full web interface:")
    print("   streamlit run app.py")
    print("\n📋 Key Features Demonstrated:")
    print("   • Natural language question processing")
    print("   • Multi-dataset query integration")
    print("   • Source citation and traceability")
    print("   • Real-time data processing")
    print("   • Swiss design aesthetic interface")

if __name__ == "__main__":
    demo_system()

