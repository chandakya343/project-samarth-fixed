"""
Gemini Client for Project Samarth
Handles all LLM calls to Google Gemini with XML-structured prompts
"""

import google.generativeai as genai
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not provided")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create logs directory
        os.makedirs('llm_logs', exist_ok=True)
    
    def call_llm(self, prompt: str, call_type: str) -> Dict[str, Any]:
        """
        Make a single LLM call and log everything
        
        Args:
            prompt: Full XML-structured prompt
            call_type: 'query_generation' or 'answer_synthesis'
        
        Returns:
            Dict with response text and metadata
        """
        timestamp = datetime.now().isoformat()
        log_id = f"{call_type}_{timestamp.replace(':', '-')}"
        
        # Log input
        input_log = {
            'timestamp': timestamp,
            'call_type': call_type,
            'prompt': prompt,
            'model': 'gemini-1.5-flash'
        }
        
        try:
            with open(f'llm_logs/{log_id}_INPUT.json', 'w', encoding='utf-8') as f:
                json.dump(input_log, f, indent=2, ensure_ascii=False)
            
            # Also save raw prompt
            with open(f'llm_logs/{log_id}_INPUT_RAW.txt', 'w', encoding='utf-8') as f:
                f.write(prompt)
        except Exception as e:
            print(f"Warning: Could not save input logs: {str(e)}")
        
        # Make LLM call
        try:
            response = self.model.generate_content(prompt)
            
            # Handle response safely
            if response is None:
                response_text = "Error: API returned None response"
            elif hasattr(response, 'text') and response.text:
                response_text = response.text
            elif hasattr(response, 'parts') and response.parts and len(response.parts) > 0:
                response_text = response.parts[0].text
            elif hasattr(response, 'candidates') and response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    response_text = candidate.content.parts[0].text
                else:
                    response_text = f"Error: Unable to extract text from response structure: {str(response)}"
            else:
                response_text = f"Error: Unexpected response format: {str(response)}"
        except Exception as e:
            response_text = f"Error generating content: {str(e)}\nFull exception: {type(e).__name__}"
        
        # Log output
        output_log = {
            'timestamp': timestamp,
            'call_type': call_type,
            'response': response_text,
            'model': 'gemini-1.5-flash'
        }
        
        try:
            with open(f'llm_logs/{log_id}_OUTPUT.json', 'w', encoding='utf-8') as f:
                json.dump(output_log, f, indent=2, ensure_ascii=False)
            
            # Also save raw response
            with open(f'llm_logs/{log_id}_OUTPUT_RAW.txt', 'w', encoding='utf-8') as f:
                f.write(response_text)
        except Exception as e:
            print(f"Warning: Could not save output logs: {str(e)}")
        
        return {
            'response': response_text,
            'log_id': log_id,
            'timestamp': timestamp
        }

