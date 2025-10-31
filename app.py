"""
Streamlit Frontend for Project Samarth
Simple web interface for asking agricultural and climate questions
"""

import streamlit as st
import os
from qa_system import AgriculturalQASystem
import json

# Page configuration
st.set_page_config(
    page_title="Project Samarth - Agricultural Q&A System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Swiss design aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.1em;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    .question-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    
    .answer-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #27ae60;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .source-box {
        background-color: #ecf0f1;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'qa_system' not in st.session_state:
        st.session_state.qa_system = None
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'datasets_info' not in st.session_state:
        st.session_state.datasets_info = None

def load_qa_system():
    """Load the Q&A system"""
    if st.session_state.qa_system is None:
        with st.spinner("Loading agricultural data and initializing Q&A system..."):
            try:
                # Get OpenAI API key from environment or user input
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    api_key = st.sidebar.text_input(
                        "OpenAI API Key (optional)", 
                        type="password",
                        help="Enter your OpenAI API key for enhanced responses. Leave empty for basic functionality."
                    )
                
                st.session_state.qa_system = AgriculturalQASystem(api_key)
                st.session_state.datasets_info = st.session_state.qa_system.get_available_datasets()
                st.success("✅ System loaded successfully!")
            except Exception as e:
                st.error(f"❌ Error loading system: {str(e)}")
                return False
    return True

def display_dataset_info():
    """Display information about available datasets"""
    if st.session_state.datasets_info:
        st.sidebar.markdown("### 📊 Available Datasets")
        
        for name, info in st.session_state.datasets_info.items():
            with st.sidebar.expander(f"📁 {name.replace('_', ' ').title()}"):
                st.write(f"**Shape:** {info['shape']}")
                st.write(f"**Description:** {info['description']}")
                st.write(f"**Columns:** {len(info['columns'])}")

def display_sample_questions():
    """Display sample questions"""
    sample_questions = [
        "How many mandis are there in Punjab?",
        "What are the neighboring districts of Delhi?", 
        "List the top 5 crops available in the Agmark system",
        "Show me all districts in Maharashtra",
        "Which states have the most agricultural markets?",
        "What crops are available in the Agmark system?"
    ]
    
    st.markdown("### 💡 Sample Questions")
    for i, question in enumerate(sample_questions):
        if st.button(f"Q{i+1}: {question}", key=f"sample_{i}"):
            st.session_state.user_question = question
            st.rerun()

def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">Project Samarth</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Intelligent Q&A System for Indian Agricultural & Climate Data</p>', unsafe_allow_html=True)
    
    # Load Q&A system
    if not load_qa_system():
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 About")
        st.markdown("""
        This system answers questions about Indian agricultural markets, crops, locations, and climate data using government datasets.
        
        **Data Sources:**
        - Agmark mandis and locations
        - Crop varieties and types  
        - District hierarchies and neighbors
        - IMD weather advisory locations
        """)
        
        display_dataset_info()
        
        # System metrics
        if st.session_state.datasets_info:
            total_records = sum(info['shape'][0] for info in st.session_state.datasets_info.values())
            st.markdown("### 📈 System Stats")
            st.metric("Total Records", f"{total_records:,}")
            st.metric("Datasets", len(st.session_state.datasets_info))
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Question input
        st.markdown("### 🤔 Ask a Question")
        user_question = st.text_area(
            "Enter your question about Indian agricultural or climate data:",
            value=st.session_state.get('user_question', ''),
            height=100,
            placeholder="e.g., How many mandis are there in Punjab?"
        )
        
        # Process question
        if st.button("🔍 Get Answer", type="primary") and user_question:
            with st.spinner("Processing your question..."):
                try:
                    result = st.session_state.qa_system.ask_question(user_question)
                    
                    if result['success']:
                        # Display answer
                        st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                        st.markdown("### 📋 Answer")
                        st.write(result['answer'])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display sources
                        if result['sources']:
                            st.markdown("### 📚 Data Sources")
                            for source in result['sources']:
                                st.markdown(f'<div class="source-box">📄 {source}</div>', unsafe_allow_html=True)
                        
                        # Add to conversation history
                        st.session_state.conversation_history.append({
                            'question': user_question,
                            'answer': result['answer'],
                            'sources': result['sources']
                        })
                        
                        # Show raw data (collapsible)
                        with st.expander("🔍 View Raw Data"):
                            st.json(result['raw_data'])
                            
                    else:
                        st.error(f"❌ Error: {result['answer']}")
                        
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
    
    with col2:
        # Sample questions
        display_sample_questions()
        
        # Conversation history
        if st.session_state.conversation_history:
            st.markdown("### 💬 Recent Questions")
            for i, conv in enumerate(reversed(st.session_state.conversation_history[-5:])):
                with st.expander(f"Q: {conv['question'][:50]}..."):
                    st.write(conv['answer'][:200] + "...")
                    if st.button(f"Ask Again", key=f"repeat_{i}"):
                        st.session_state.user_question = conv['question']
                        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
        Project Samarth - Built for the Government Data Challenge<br>
        Powered by OpenAI GPT and Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

