"""
Main Q&A System for Project Samarth
Integrates query generation, execution, and response formatting
"""

import json
from typing import Dict, Any, List
from query_generator import PandasQueryGenerator
from data_loader import AgriculturalDataLoader

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AgriculturalQASystem:
    def __init__(self, openai_api_key: str = None):
        self.query_generator = PandasQueryGenerator(openai_api_key)
        self.data_loader = AgriculturalDataLoader()
        self.data_loader.load_all_data()
        
    def ask_question(self, question: str, max_results: int = 20) -> Dict[str, Any]:
        """
        Main method to process a question and return a comprehensive answer
        """
        print(f"Processing question: {question}")
        
        # Step 1: Generate pandas query
        query_result = self.query_generator.generate_query(question, max_results)
        
        if not query_result['success']:
            return {
                "question": question,
                "answer": f"I encountered an error generating the query: {query_result.get('error', 'Unknown error')}",
                "sources": [],
                "success": False
            }
        
        # Step 2: Execute the query
        exec_result = self.query_generator.execute_query(query_result['query_code'])
        
        if not exec_result['success']:
            return {
                "question": question,
                "answer": f"I encountered an error executing the query: {exec_result.get('error', 'Unknown error')}",
                "sources": [],
                "success": False
            }
        
        # Step 3: Format the data for LLM response generation
        formatted_data = self._format_query_results(exec_result['data'])
        
        # Step 4: Generate final answer using LLM
        final_answer = self._generate_final_answer(question, formatted_data, query_result['query_code'])
        
        # Step 5: Identify data sources
        sources = self._identify_sources(query_result['query_code'])
        
        return {
            "question": question,
            "answer": final_answer,
            "sources": sources,
            "query_code": query_result['query_code'],
            "raw_data": exec_result['data'],
            "success": True
        }
    
    def _format_query_results(self, data: Any) -> str:
        """Format query results for LLM consumption"""
        if isinstance(data, list):
            # Single dataframe result
            if len(data) > 20:
                data = data[:20]  # Limit to top 20 results
            return f"Query Results ({len(data)} records):\n{json.dumps(data, indent=2)}"
        
        elif isinstance(data, dict):
            # Multiple dataframe results
            formatted = "Query Results:\n"
            for key, value in data.items():
                if isinstance(value, dict) and 'data' in value:
                    records = value['data'][:10]  # Limit each dataset to 10 records
                    formatted += f"\n{key.upper()} ({len(records)} records):\n"
                    formatted += json.dumps(records, indent=2)
            return formatted
        
        else:
            return f"Query Results: {str(data)}"
    
    def _generate_final_answer(self, question: str, formatted_data: str, query_code: str) -> str:
        """Generate final answer using LLM"""
        prompt = f"""
You are an expert agricultural data analyst. Based on the query results below, provide a comprehensive answer to the user's question.

USER QUESTION: {question}

QUERY EXECUTED:
{query_code}

QUERY RESULTS:
{formatted_data}

INSTRUCTIONS:
1. Analyze the data and provide a clear, accurate answer to the question
2. Include specific numbers, names, and details from the data
3. If the data shows trends or patterns, mention them
4. If the question asks for comparisons, make them explicit
5. Be concise but comprehensive
6. Always cite specific data points from the results
7. If the data is insufficient to fully answer the question, explain what information is available and what's missing

Provide your answer:
"""

        try:
            if OPENAI_AVAILABLE and self.query_generator.client:
                response = self.query_generator.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=1000
                )
                return response.choices[0].message.content.strip()
            else:
                # Fallback to simple data summary
                return self._generate_fallback_answer(question, formatted_data)
                
        except Exception as e:
            return f"I generated the data but encountered an error creating the final answer: {str(e)}. Here's the raw data: {formatted_data[:500]}..."
    
    def _generate_fallback_answer(self, question: str, formatted_data: str) -> str:
        """Fallback answer generation"""
        return f"""
Based on the available data, here's what I found:

{formatted_data[:800]}

Note: This is a summary of the raw data. For a more detailed analysis, please provide an OpenAI API key to enable advanced natural language processing.
"""
    
    def _identify_sources(self, query_code: str) -> List[str]:
        """Identify which datasets were used in the query"""
        sources = []
        
        # Map dataframe names to human-readable source names
        source_mapping = {
            'agmark_mandis_and_locations': 'Agmark Mandis and Locations Dataset',
            'location_hierarchy': 'Location Hierarchy Dataset', 
            'district_neighbour_map_india': 'District Neighbour Map Dataset',
            'mandi_apmc_map': 'APMC Mandi Map Dataset',
            'agmark_crops': 'Agmark Crops Dataset',
            'imd_agromet_advisory_locations': 'IMD Agromet Advisory Locations Dataset'
        }
        
        for df_name, source_name in source_mapping.items():
            if df_name in query_code.lower():
                sources.append(source_name)
        
        return sources
    
    def get_available_datasets(self) -> Dict[str, Any]:
        """Get information about available datasets"""
        datasets = {}
        for df_name in self.data_loader.list_dataframes():
            df = self.data_loader.get_dataframe(df_name)
            datasets[df_name] = {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "description": self._get_dataset_description(df_name)
            }
        return datasets
    
    def _get_dataset_description(self, df_name: str) -> str:
        """Get human-readable description of dataset"""
        descriptions = {
            'agmark_mandis_and_locations': 'Agricultural markets (mandis) across India with location mapping',
            'location_hierarchy': 'Complete hierarchy of states, divisions, districts, and blocks',
            'district_neighbour_map_india': 'Mapping of neighboring districts for each district in India',
            'mandi_apmc_map': 'APMC (Agricultural Produce Market Committee) mandi mappings',
            'agmark_crops': 'Crop varieties and types available in Agmark system',
            'imd_agromet_advisory_locations': 'IMD weather advisory locations and access links'
        }
        return descriptions.get(df_name, 'Agricultural and climate data')

# Example usage and testing
if __name__ == "__main__":
    # Initialize the Q&A system
    qa_system = AgriculturalQASystem()
    
    # Test questions
    test_questions = [
        "How many mandis are there in Punjab?",
        "What are the neighboring districts of Delhi?",
        "List the top 5 crops available in the Agmark system",
        "Show me all districts in Maharashtra"
    ]
    
    print("Available datasets:")
    datasets = qa_system.get_available_datasets()
    for name, info in datasets.items():
        print(f"- {name}: {info['shape']} - {info['description']}")
    
    print("\n" + "="*50)
    print("TESTING Q&A SYSTEM")
    print("="*50)
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        result = qa_system.ask_question(question)
        
        if result['success']:
            print(f"Answer: {result['answer']}")
            print(f"Sources: {', '.join(result['sources'])}")
        else:
            print(f"Error: {result['answer']}")
        
        print("-" * 30)
