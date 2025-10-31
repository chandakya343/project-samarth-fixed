"""
Main Pipeline for Project Samarth
Orchestrates the 2-LLM call architecture
"""

import json
from datetime import datetime
from typing import Dict, Any
from query_generator_gemini import QueryGeneratorGemini
from executor import QueryExecutor
from answer_synthesizer import AnswerSynthesizer

class SamarthPipeline:
    def __init__(self, gemini_api_key: str):
        self.query_generator = QueryGeneratorGemini(gemini_api_key)
        self.executor = QueryExecutor()
        self.answer_synthesizer = AnswerSynthesizer(gemini_api_key)
    
    def process_question(self, question: str) -> Dict[str, Any]:
        """
        Process a single question through the full pipeline
        
        Pipeline:
        1. Query Generation (LLM Call #1)
        2. Query Execution (Deterministic)
        3. Evidence Building (Deterministic)
        4. Citation Building (Deterministic)
        5. Answer Synthesis (LLM Call #2)
        6. Save complete trace
        """
        trace = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'steps': []
        }
        
        # Step 1: Query Generation (LLM Call #1)
        print("Step 1: Generating pandas query...")
        query_result = self.query_generator.generate_query(question)
        
        # Check for errors in query generation
        if 'error' in query_result or query_result.get('query_code') is None:
            error_msg = query_result.get('error', 'Failed to generate query')
            trace['steps'].append({
                'step': 1,
                'name': 'Query Generation (LLM Call #1)',
                'error': error_msg
            })
            trace['final_answer'] = f"Error generating query: {error_msg}"
            self._save_trace(trace)
            return {
                'success': False,
                'error': error_msg,
                'trace': trace
            }
        
        trace['steps'].append({
            'step': 1,
            'name': 'Query Generation (LLM Call #1)',
            'log_id': query_result.get('log_id', 'unknown'),
            'query_code': query_result.get('query_code', ''),
            'relevant_datasets': query_result.get('relevant_datasets', [])
        })
        print(f"✓ Generated query (log: {query_result.get('log_id', 'unknown')})")
        
        # Step 2: Query Execution (Deterministic)
        print("Step 2: Executing query...")
        exec_result = self.executor.execute_query(query_result['query_code'])
        
        if not exec_result['success']:
            trace['steps'].append({
                'step': 2,
                'name': 'Query Execution',
                'error': exec_result['error']
            })
            trace['final_answer'] = f"Error executing query: {exec_result['error']}"
            self._save_trace(trace)
            return {
                'success': False,
                'error': exec_result['error'],
                'trace': trace
            }
        
        trace['steps'].append({
            'step': 2,
            'name': 'Query Execution (Deterministic)',
            'evidence_summary': {
                'type': exec_result['evidence']['type'],
                'shape': exec_result['evidence']['shape'],
                'summary_stats': exec_result['evidence']['summary_stats']
            }
        })
        print(f"✓ Query executed successfully")
        
        # Step 3: Citation Building (Deterministic)
        print("Step 3: Building citations...")
        citations = self.executor.build_citations(exec_result['evidence']['datasets_used'])
        trace['steps'].append({
            'step': 3,
            'name': 'Citation Building (Deterministic)',
            'citations': citations
        })
        print(f"✓ Built {len(citations)} citations")
        
        # Step 4: Answer Synthesis (LLM Call #2)
        print("Step 4: Synthesizing answer...")
        synthesis_result = self.answer_synthesizer.synthesize_answer(
            question=question,
            executed_code=exec_result['executed_code'],
            evidence=exec_result['evidence'],
            citations=citations
        )
        trace['steps'].append({
            'step': 4,
            'name': 'Answer Synthesis (LLM Call #2)',
            'log_id': synthesis_result['log_id']
        })
        print(f"✓ Answer synthesized (log: {synthesis_result['log_id']})")
        
        # Final result
        trace['final_answer'] = synthesis_result['answer']
        trace['citations'] = citations
        
        # Save complete trace
        self._save_trace(trace)
        
        return {
            'success': True,
            'question': question,
            'answer': synthesis_result['answer'],
            'citations': citations,
            'trace': trace
        }
    
    def _save_trace(self, trace: Dict[str, Any]):
        """Save complete execution trace"""
        try:
            import os
            os.makedirs('llm_logs', exist_ok=True)
            
            timestamp = trace['timestamp'].replace(':', '-')
            filename = f"llm_logs/TRACE_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(trace, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Trace saved: {filename}")
        except Exception as e:
            print(f"Warning: Could not save trace: {str(e)}")

