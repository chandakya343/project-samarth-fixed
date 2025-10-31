"""
Data Loader Module for Project Samarth
Loads and preprocesses agricultural and climate data from bolbhav-data repository
"""

import pandas as pd
import os
from typing import Dict, List, Any
import json

class AgriculturalDataLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.dataframes = {}
        self.schema_info = {}
        
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all available datasets"""
        print("Loading agricultural and climate data...")
        
        # Load CSV files
        csv_files = [
            "Agmark Mandis and locations.csv",
            "Location hierarchy.csv", 
            "District Neighbour Map India.csv",
            "Mandi (APMC) Map.csv"
        ]
        
        for file in csv_files:
            file_path = os.path.join(self.data_dir, file)
            if os.path.exists(file_path):
                df_name = file.replace(".csv", "").replace(" ", "_").replace("(", "").replace(")", "").lower()
                self.dataframes[df_name] = pd.read_csv(file_path)
                print(f"Loaded {file}: {self.dataframes[df_name].shape}")
        
        # Load Excel files
        excel_files = [
            "Agmark crops.xlsx",
            "IMD Agromet advisory locations.xlsx"
        ]
        
        for file in excel_files:
            file_path = os.path.join(self.data_dir, file)
            if os.path.exists(file_path):
                df_name = file.replace(".xlsx", "").replace(" ", "_").replace("(", "").replace(")", "").lower()
                self.dataframes[df_name] = pd.read_excel(file_path)
                print(f"Loaded {file}: {self.dataframes[df_name].shape}")
        
        # Generate schema information for each dataframe
        self._generate_schema_info()
        
        return self.dataframes
    
    def _generate_schema_info(self):
        """Generate detailed schema information for LLM context"""
        for df_name, df in self.dataframes.items():
            schema = {
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.to_dict(),
                "shape": df.shape,
                "sample_data": df.head(3).to_dict('records'),
                "null_counts": df.isnull().sum().to_dict(),
                "unique_counts": df.nunique().to_dict()
            }
            self.schema_info[df_name] = schema
    
    def get_schema_context(self) -> str:
        """Generate comprehensive schema context for LLM prompts"""
        context = "DATABASE SCHEMA INFORMATION:\n\n"
        
        for df_name, schema in self.schema_info.items():
            context += f"=== {df_name.upper()} ===\n"
            context += f"Shape: {schema['shape']}\n"
            context += f"Columns: {schema['columns']}\n"
            context += f"Data Types: {schema['dtypes']}\n"
            context += f"Sample Data:\n{json.dumps(schema['sample_data'], indent=2)}\n"
            context += f"Unique Values per Column: {schema['unique_counts']}\n\n"
        
        return context
    
    def get_dataframe(self, name: str) -> pd.DataFrame:
        """Get a specific dataframe by name"""
        return self.dataframes.get(name)
    
    def list_dataframes(self) -> List[str]:
        """List all available dataframe names"""
        return list(self.dataframes.keys())
    
    def search_dataframes(self, query: str) -> List[str]:
        """Search for dataframes that might contain relevant information"""
        query_lower = query.lower()
        relevant_dfs = []
        
        for df_name in self.dataframes.keys():
            if any(keyword in df_name for keyword in ['mandi', 'location', 'crop', 'district', 'state', 'imd']):
                relevant_dfs.append(df_name)
        
        return relevant_dfs

# Example usage and testing
if __name__ == "__main__":
    loader = AgriculturalDataLoader()
    dataframes = loader.load_all_data()
    
    print("\nAvailable datasets:")
    for name in loader.list_dataframes():
        print(f"- {name}: {dataframes[name].shape}")
    
    print("\nSchema context:")
    print(loader.get_schema_context()[:1000] + "...")

