"""
Query Executor - Deterministic code execution and evidence building
"""

import pandas as pd
import json
from typing import Dict, Any, List
from data_loader import AgriculturalDataLoader

class QueryExecutor:
    def __init__(self):
        self.data_loader = AgriculturalDataLoader()
        self.data_loader.load_all_data()
    
    def execute_query(self, query_code: str, max_results: int = 20) -> Dict[str, Any]:
        """
        Execute pandas query and build evidence bundle
        Pure deterministic execution
        """
        try:
            # Create safe execution environment
            safe_globals = {
                'data_loader': self.data_loader,
                'pd': pd,
                'result': None
            }
            
            # Execute query
            exec(query_code, safe_globals)
            
            result = safe_globals.get('result')
            
            if result is None:
                return {
                    'success': False,
                    'error': 'No result variable found in query'
                }
            
            # Build evidence bundle
            evidence = self._build_evidence(result, query_code, max_results)
            
            return {
                'success': True,
                'evidence': evidence,
                'executed_code': query_code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'executed_code': query_code
            }
    
    def _build_evidence(self, result: Any, query_code: str, max_results: int) -> Dict[str, Any]:
        """Build structured evidence bundle from query result"""
        evidence = {
            'type': None,
            'shape': None,
            'columns': None,
            'records': None,
            'summary_stats': {},
            'datasets_used': self._extract_datasets_used(query_code)
        }
        
        if isinstance(result, pd.DataFrame):
            evidence['type'] = 'DataFrame'
            evidence['shape'] = result.shape
            evidence['columns'] = result.columns.tolist()
            
            # Cap to max_results
            capped_result = result.head(max_results)
            evidence['records'] = capped_result.to_dict('records')
            
            # Add summary stats
            evidence['summary_stats'] = {
                'total_rows': len(result),
                'rows_returned': len(capped_result),
                'capped': len(result) > max_results
            }
            
        elif isinstance(result, pd.Series):
            evidence['type'] = 'Series'
            evidence['shape'] = result.shape
            evidence['records'] = result.head(max_results).to_dict()
            evidence['summary_stats'] = {
                'total_items': len(result),
                'items_returned': min(len(result), max_results),
                'capped': len(result) > max_results
            }
            
        else:
            evidence['type'] = 'Other'
            evidence['records'] = str(result)
        
        return evidence
    
    def _extract_datasets_used(self, query_code: str) -> List[str]:
        """Extract dataset names used in the query (deterministic)"""
        datasets = []
        
        # Look for data_loader.get_dataframe('dataset_name') patterns
        import re
        matches = re.findall(r"get_dataframe\(['\"]([^'\"]+)['\"]\)", query_code)
        datasets.extend(matches)
        
        return list(set(datasets))
    
    def build_citations(self, datasets_used: List[str]) -> List[Dict[str, str]]:
        """Build citation information (deterministic)"""
        citations = []
        
        dataset_info = {
            'agmark_mandis_and_locations': {
                'name': 'Agmark Mandis and Locations Dataset',
                'source': 'Agmarknet (agmarknet.gov.in)',
                'description': 'Agricultural markets (mandis) across India'
            },
            'location_hierarchy': {
                'name': 'Location Hierarchy Dataset',
                'source': 'Government administrative data',
                'description': 'State-Division-District-Block hierarchy'
            },
            'district_neighbour_map_india': {
                'name': 'District Neighbour Map Dataset',
                'source': 'Geographic administrative data',
                'description': 'Neighboring districts mapping'
            },
            'mandi_apmc_map': {
                'name': 'APMC Mandi Map Dataset',
                'source': 'APMC (Agricultural Produce Market Committee)',
                'description': 'APMC mandi mappings'
            },
            'agmark_crops': {
                'name': 'Agmark Crops Dataset',
                'source': 'Agmarknet (agmarknet.gov.in)',
                'description': 'Crop varieties and types'
            },
            'imd_agromet_advisory_locations': {
                'name': 'IMD Agromet Advisory Locations Dataset',
                'source': 'India Meteorological Department (IMD)',
                'description': 'Weather advisory locations'
            }
        }
        
        for dataset in datasets_used:
            if dataset in dataset_info:
                citations.append(dataset_info[dataset])
        
        return citations

