"""
Query Generator using Gemini
LLM Call #1: Understanding + Query Generation
"""

import re
from typing import Dict, Any
from gemini_client import GeminiClient
from schema_builder import SchemaBuilder

class QueryGeneratorGemini:
    def __init__(self, api_key: str):
        self.gemini = GeminiClient(api_key)
        self.schema_builder = SchemaBuilder()
        self.max_results = 20
    
    def generate_query(self, question: str) -> Dict[str, Any]:
        """
        LLM Call #1: Generate pandas query from natural language question
        
        Returns:
            Dict with query_code, relevant_datasets, log_id
        """
        try:
            # Step 1: Determine relevant datasets
            relevant_datasets = self.schema_builder.get_relevant_datasets(question)
            
            # Step 2: Build schema XML for those datasets
            schema_xml = self.schema_builder.build_schema_xml(relevant_datasets)
            
            # Step 3: Build full XML prompt
            prompt = self._build_query_generation_prompt(question, schema_xml)
            
            # Step 4: Call LLM
            response = self.gemini.call_llm(prompt, 'query_generation')
            
            # Step 5: Validate response
            if response is None:
                raise ValueError("LLM returned None response")
            
            if 'response' not in response:
                raise ValueError("LLM response missing 'response' key")
            
            # Step 6: Extract pandas code from response
            query_code = self._extract_pandas_code(response['response'])
            
            if not query_code or query_code.strip() == "":
                raise ValueError("Failed to extract pandas code from LLM response")
            
            return {
                'query_code': query_code,
                'relevant_datasets': relevant_datasets,
                'log_id': response.get('log_id', 'unknown'),
                'raw_response': response.get('response', '')
            }
        except Exception as e:
            return {
                'query_code': None,
                'relevant_datasets': [],
                'log_id': 'error',
                'error': str(e),
                'raw_response': ''
            }
    
    def _build_query_generation_prompt(self, question: str, schema_xml: str) -> str:
        """Build XML-structured prompt for query generation"""
        prompt = f"""<SYSTEM>You are a senior data analyst who writes precise pandas queries.</SYSTEM>

{schema_xml}

<QUESTION>
{question}
</QUESTION>

<CONSTRAINTS>
- Use exact dataframe names and column names as shown in <SCHEMA>
- Access dataframes using: data_loader.get_dataframe('dataset_name')
- Prefer boolean masking, groupby/agg, sort_values
- Always cap outputs with .head({self.max_results})
- Avoid joins unless necessary; if joining, explain key columns
- Handle null values appropriately
- Use .str.contains() with case=False for string matching
- Return a single code block that assigns final result to variable named 'result'
</CONSTRAINTS>

<OUTPUT_FORMAT>
Return only the pandas code inside <PANDAS_CODE> tags.
Example:
<PANDAS_CODE>
# Get mandis in Punjab
mandis_df = data_loader.get_dataframe('agmark_mandis_and_locations')
result = mandis_df[mandis_df['State Name'].str.contains('Punjab', case=False)].head({self.max_results})
</PANDAS_CODE>
</OUTPUT_FORMAT>"""
        
        return prompt
    
    def _extract_pandas_code(self, response: str) -> str:
        """Extract code from <PANDAS_CODE> tags"""
        match = re.search(r'<PANDAS_CODE>(.*?)</PANDAS_CODE>', response, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # Fallback: try to find code blocks
        match = re.search(r'```python(.*?)```', response, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # Last resort: return raw response
        return response.strip()

