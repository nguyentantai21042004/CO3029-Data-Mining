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
        default_numeric = ['value', 'avg', 'average', 'temp', 'rain', 'yield', 'tonnes']
        
        # If numeric_columns not specified, try to detect numeric columns
        if numeric_columns is None:
            # Read first few rows to detect column types
            df_sample = pd.read_csv(file_path, nrows=5)
            numeric_columns = []
            for col in df_sample.columns:
                # Check if column name contains numeric indicators
                if any(indicator in col.lower() for indicator in default_numeric):
                    numeric_columns.append(col)
                # Check if column values are numeric
                elif pd.to_numeric(df_sample[col], errors='coerce').notna().all():
                    numeric_columns.append(col)
        
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
        
        # Load data
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Convert numeric columns
        if numeric_columns:
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