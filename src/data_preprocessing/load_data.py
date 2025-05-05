"""
Module for loading data from various sources.
"""
import pandas as pd #type: ignore
from utils.logging import logger
from typing import Optional, List

def load_csv(file_path: str, 
             numeric_columns: Optional[List[str]] = None,
             date_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        numeric_columns (List[str], optional): List of columns that should be numeric
        date_columns (List[str], optional): List of columns that should be dates
        
    Returns:
        pd.DataFrame: Loaded dataframe
    """
    try:
        logger.info(f"Attempting to load CSV file: {file_path}")
        
        # Define default numeric columns based on common patterns
        default_numeric = [
            'Year', 'Average_Temperature_C', 'Total_Precipitation_mm',
            'CO2_Emissions_MT', 'Crop_Yield_MT_per_HA', 'Extreme_Weather_Events',
            'Irrigation_Access_%', 'Pesticide_Use_KG_per_HA', 'Fertilizer_Use_KG_per_HA',
            'Soil_Health_Index', 'Economic_Impact_Million_USD'
        ]
        
        # If numeric_columns not specified, use default
        if numeric_columns is None:
            numeric_columns = default_numeric
        
        # Load data with proper type conversion
        df = pd.read_csv(file_path)
        
        # Convert numeric columns
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert date columns
        if date_columns:
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
        
        logger.info(f"Successfully loaded CSV file with shape: {df.shape}")
        return df
        
    except Exception as e:
        logger.error(f"Error loading CSV file: {str(e)}")
        raise

def load_excel(file_path: str, 
               sheet_name: Optional[str] = None,
               numeric_columns: Optional[List[str]] = None,
               date_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Load data from an Excel file.
    
    Args:
        file_path (str): Path to the Excel file
        sheet_name (str, optional): Name of the sheet to load
        numeric_columns (List[str], optional): List of columns that should be numeric
        date_columns (List[str], optional): List of columns that should be dates
        
    Returns:
        pd.DataFrame: Loaded dataframe
    """
    try:
        logger.info(f"Attempting to load Excel file: {file_path}")
        
        # Define default numeric columns
        default_numeric = [
            'Year', 'Average_Temperature_C', 'Total_Precipitation_mm',
            'CO2_Emissions_MT', 'Crop_Yield_MT_per_HA', 'Extreme_Weather_Events',
            'Irrigation_Access_%', 'Pesticide_Use_KG_per_HA', 'Fertilizer_Use_KG_per_HA',
            'Soil_Health_Index', 'Economic_Impact_Million_USD'
        ]
        
        # If numeric_columns not specified, use default
        if numeric_columns is None:
            numeric_columns = default_numeric
        
        # Load data
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Convert numeric columns
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert date columns
        if date_columns:
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
        
        logger.info(f"Successfully loaded Excel file with shape: {df.shape}")
        return df
        
    except Exception as e:
        logger.error(f"Error loading Excel file: {str(e)}")
        raise