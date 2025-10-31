"""
Schema Builder for Project Samarth
Builds minimal schema context for LLM prompts
"""

import pandas as pd
from typing import Dict, List
from data_loader import AgriculturalDataLoader

class SchemaBuilder:
    def __init__(self):
        self.data_loader = AgriculturalDataLoader()
        self.data_loader.load_all_data()
    
    def get_relevant_datasets(self, question: str) -> List[str]:
        """
        Determine which datasets are relevant to the question
        Simple keyword matching for now
        """
        question_lower = question.lower()
        relevant = []
        
        keywords_map = {
            'agmark_mandis_and_locations': ['mandi', 'market', 'agmark', 'state', 'district', 'location'],
            'location_hierarchy': ['district', 'block', 'state', 'division', 'hierarchy', 'administrative'],
            'district_neighbour_map_india': ['neighbor', 'neighbour', 'adjacent', 'nearby', 'border'],
            'mandi_apmc_map': ['apmc', 'mandi', 'market'],
            'agmark_crops': ['crop', 'variety', 'wheat', 'rice', 'paddy', 'maize', 'vegetable', 'fruit'],
            'imd_agromet_advisory_locations': ['weather', 'imd', 'climate', 'advisory', 'forecast']
        }
        
        for df_name, keywords in keywords_map.items():
            if any(kw in question_lower for kw in keywords):
                relevant.append(df_name)
        
        # If nothing matched, return all datasets
        if not relevant:
            relevant = list(self.data_loader.list_dataframes())
        
        return relevant
    
    def build_schema_xml(self, dataset_names: List[str]) -> str:
        """
        Build XML-formatted schema context for specified datasets
        """
        schema_xml = "<SCHEMA>\n"
        
        for df_name in dataset_names:
            df = self.data_loader.get_dataframe(df_name)
            if df is None:
                continue
            
            schema_xml += f"  <DATASET name=\"{df_name}\">\n"
            schema_xml += f"    <row_count>{len(df)}</row_count>\n"
            schema_xml += "    <columns>\n"
            
            for col in df.columns:
                dtype = str(df[col].dtype)
                unique_count = df[col].nunique()
                null_count = df[col].isnull().sum()
                
                schema_xml += f"      <column name=\"{col}\" dtype=\"{dtype}\" unique=\"{unique_count}\" nulls=\"{null_count}\"/>\n"
            
            schema_xml += "    </columns>\n"
            schema_xml += "    <sample_rows>\n"
            
            # Get 2-3 sample rows
            sample_rows = df.head(3).to_dict('records')
            for i, row in enumerate(sample_rows):
                schema_xml += f"      <row index=\"{i}\">\n"
                for key, value in row.items():
                    # Escape XML special characters
                    value_str = str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    schema_xml += f"        <field name=\"{key}\">{value_str}</field>\n"
                schema_xml += "      </row>\n"
            
            schema_xml += "    </sample_rows>\n"
            schema_xml += "  </DATASET>\n\n"
        
        schema_xml += "</SCHEMA>"
        return schema_xml

