"""
Answer Synthesizer using Gemini
LLM Call #2: Context Manager + Answer Synthesis
"""

import json
from typing import Dict, Any, List
from gemini_client import GeminiClient

class AnswerSynthesizer:
    def __init__(self, api_key: str):
        self.gemini = GeminiClient(api_key)
    
    def synthesize_answer(
        self, 
        question: str, 
        executed_code: str, 
        evidence: Dict[str, Any],
        citations: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        LLM Call #2: Synthesize final answer from evidence
        
        Returns:
            Dict with answer, citations, log_id
        """
        # Build XML prompt
        prompt = self._build_synthesis_prompt(question, executed_code, evidence, citations)
        
        # Call LLM
        response = self.gemini.call_llm(prompt, 'answer_synthesis')
        
        return {
            'answer': response['response'],
            'citations': citations,
            'log_id': response['log_id'],
            'raw_response': response['response']
        }
    
    def _build_synthesis_prompt(
        self, 
        question: str, 
        executed_code: str, 
        evidence: Dict[str, Any],
        citations: List[Dict[str, str]]
    ) -> str:
        """Build XML-structured prompt for answer synthesis"""
        
        # Format evidence as clean JSON
        evidence_json = json.dumps(evidence, indent=2, ensure_ascii=False)
        
        # Format citations
        citations_xml = "<CITATIONS>\n"
        for citation in citations:
            citations_xml += f"  <SOURCE>\n"
            citations_xml += f"    <name>{citation['name']}</name>\n"
            citations_xml += f"    <source>{citation['source']}</source>\n"
            citations_xml += f"    <description>{citation['description']}</description>\n"
            citations_xml += f"  </SOURCE>\n"
        citations_xml += "</CITATIONS>"
        
        prompt = f"""<SYSTEM>You are a precise policy/data analyst. Cite exact numbers and sources.</SYSTEM>

<QUESTION>
{question}
</QUESTION>

<EXECUTED_CODE>
{executed_code}
</EXECUTED_CODE>

<EVIDENCE>
{evidence_json}
</EVIDENCE>

{citations_xml}

<INSTRUCTIONS>
- Use only data from <EVIDENCE>; do not invent values
- Include explicit comparisons/trends if relevant
- Call out data gaps/limits (row caps, missing fields)
- Keep answer compact; use bullets where helpful
- Be specific with numbers and names from the evidence
- If evidence shows the data was capped, mention "showing top N results"
</INSTRUCTIONS>

<OUTPUT_FORMAT>
Provide a concise answer paragraph or bullets, then end with:

Sources:
- [List source names from <CITATIONS>]
</OUTPUT_FORMAT>"""
        
        return prompt

