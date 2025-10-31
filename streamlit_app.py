"""
Streamlit Frontend for Project Samarth
Clean interface for agricultural Q&A system
"""

import streamlit as st
import os
from dotenv import load_dotenv
from project_samarth.pipeline import SamarthPipeline
from project_samarth.data_loader import AgriculturalDataLoader

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="Project Samarth - Agricultural Q&A",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: 0.1em;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    .answer-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #27ae60;
        margin: 1rem 0;
    }
    .citation-box {
        background-color: #ecf0f1;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state"""
    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = None
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'question_input' not in st.session_state:
        st.session_state.question_input = ""

def set_question_input(question):
    """Callback to set the question input text."""
    st.session_state.question_input = question

def load_pipeline():
    """Load the pipeline"""
    if st.session_state.pipeline is None:
        # Try Streamlit secrets first (for cloud deployment), then environment variable (for local)
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            st.error("❌ GEMINI_API_KEY not configured. Please set it in Streamlit Cloud secrets or .env file")
            st.stop()
        
        with st.spinner("Loading agricultural data..."):
            try:
                st.session_state.pipeline = SamarthPipeline(api_key)
                st.success("✅ System ready!")
            except Exception as e:
                st.error(f"❌ Error initializing pipeline: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
                st.stop()

def display_datasets_info():
    """Display dataset information in sidebar"""
    st.sidebar.markdown("### 📊 Available Datasets")
    
    datasets_info = {
        "Agmark Mandis and Locations": {
            "records": "4,062",
            "description": "Agricultural markets (mandis) across India with state and district mapping",
            "key_fields": ["Mandi Name", "District", "State"]
        },
        "Location Hierarchy": {
            "records": "5,294",
            "description": "Complete administrative hierarchy: State → Division → District → Block",
            "key_fields": ["State", "District", "Block"]
        },
        "District Neighbour Map": {
            "records": "601",
            "description": "Neighboring districts for each district in India",
            "key_fields": ["District", "Neighbors"]
        },
        "APMC Mandi Map": {
            "records": "352",
            "description": "APMC (Agricultural Produce Market Committee) mandi mappings",
            "key_fields": ["Mandi Name", "District", "Division"]
        },
        "Agmark Crops": {
            "records": "321",
            "description": "Crop varieties with multilingual names (English, Hindi, Marathi)",
            "key_fields": ["Crop Name", "Variety", "Type"]
        },
        "IMD Weather Locations": {
            "records": "700",
            "description": "India Meteorological Department weather advisory locations",
            "key_fields": ["State", "District", "IMD Code"]
        }
    }
    
    for name, info in datasets_info.items():
        with st.sidebar.expander(f"📁 {name}"):
            st.markdown(f"**Records:** {info['records']}")
            st.markdown(f"**Description:** {info['description']}")
            st.markdown(f"**Key Fields:** {', '.join(info['key_fields'])}")

def display_sample_questions():
    """Display sample questions"""
    st.sidebar.markdown("### 💡 Sample Questions")
    
    sample_questions = [
        "How many mandis are in Punjab?",
        "Which state has more mandis: Gujarat or Maharashtra?",
        "What districts in Punjab have IMD weather coverage?",
        "Show me the top 5 crops in the Agmark system",
        "How many districts have more than 20 mandis?",
        "What are the Hindi names of vegetable crops?",
        "Which districts neighbor Delhi?",
        "List all blocks in Andhra Pradesh"
    ]
    
    for i, question in enumerate(sample_questions):
        st.sidebar.button(
            f"📌 {question}", 
            key=f"sample_{i}", 
            on_click=set_question_input, 
            args=(question,), 
            use_container_width=True
        )

def main():
    """Main app"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🌾 Project Samarth</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Intelligent Q&A System for Indian Agricultural & Climate Data</p>', unsafe_allow_html=True)
    
    # Load pipeline
    load_pipeline()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 About")
        st.markdown("""
        Ask questions about Indian agricultural markets, crops, locations, and climate data. 
        The system uses AI to understand your question and query government datasets.
        """)
        
        st.markdown("---")
        display_datasets_info()
        
        st.markdown("---")
        display_sample_questions()
        
        st.markdown("---")
        st.markdown("### 📈 System Stats")
        st.metric("Total Records", "11,330")
        st.metric("Datasets", "6")
        st.metric("States Covered", "36")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🤔 Ask Your Question")
        
        user_question = st.text_area(
            "Enter your question about Indian agricultural or climate data:",
            height=100,
            placeholder="e.g., How many mandis are there in Punjab?",
            key="question_input"
        )
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            ask_button = st.button("🔍 Ask", type="primary", use_container_width=True)
        with col_btn2:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.history = []
                st.session_state.question_input = ""
                st.rerun()
        
        if ask_button and user_question:
            with st.spinner("Processing your question..."):
                try:
                    result = st.session_state.pipeline.process_question(user_question)
                    
                    if result['success']:
                        # Prepend to history
                        st.session_state.history.insert(0, {
                            'question': user_question,
                            'answer': result['answer'],
                            'citations': result['citations']
                        })
                        # Rerun to display history and prevent re-submission
                        st.rerun()
                        
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

        # Display latest answer if it exists in history
        if st.session_state.history:
            latest_item = st.session_state.history[0]
            st.markdown("### 📋 Answer")
            st.markdown(f'<div class="answer-box">{latest_item["answer"]}</div>', unsafe_allow_html=True)

            if latest_item['citations']:
                st.markdown("### 📚 Data Sources")
                for citation in latest_item['citations']:
                    st.markdown(
                        f'<div class="citation-box">📄 <b>{citation["name"]}</b><br>'
                        f'<small>Source: {citation["source"]}</small></div>',
                        unsafe_allow_html=True
                    )
    
    with col2:
        st.markdown("### 💬 Recent Questions")
        
        if st.session_state.history:
            # Display history starting from the second item (latest is already in main panel)
            for i, item in enumerate(st.session_state.history):
                with st.expander(f"Q: {item['question'][:50]}..."):
                    st.write(item['answer'][:200] + "...")
                    st.button(
                        "Ask Again", 
                        key=f"repeat_{i}", 
                        on_click=set_question_input, 
                        args=(item['question'],)
                    )
        else:
            st.info("No questions asked yet. Try a sample question from the sidebar!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
        Project Samarth - Built for Government Data Challenge<br>
        Powered by Gemini 2.5 Flash
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

