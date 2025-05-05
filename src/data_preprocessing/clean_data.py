"""
Module for cleaning and preprocessing data.
"""
import pandas as pd #type: ignore
import numpy as np #type: ignore
from typing import List, Optional
from utils.logging import logger

def handle_missing_values(df: pd.DataFrame, 
                        strategy: str = 'mean',
                        columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Args:
        df (pd.DataFrame): Input dataframe
        strategy (str): Strategy to handle missing values ('mean', 'median', 'mode', 'drop')
        columns (List[str], optional): Columns to apply the strategy to
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    try:
        if not isinstance(df, pd.DataFrame):
            logger.error("src.data_preprocessing.clean_data.handle_missing_values: Input must be a pandas DataFrame")
            return df
            
        df = df.copy()
        if columns is None:
            columns = df.columns
            
        # Define column-specific strategies
        column_strategies = {
            'Year': 'drop',  # Drop missing years as they are critical
            'Country': 'drop',  # Drop missing countries as they are critical
            'Region': 'mode',  # Use most common region
            'Crop_Type': 'mode',  # Use most common crop type
            'Average_Temperature_C': 'mean',  # Use mean temperature
            'Total_Precipitation_mm': 'mean',  # Use mean precipitation
            'CO2_Emissions_MT': 'mean',  # Use mean emissions
            'Crop_Yield_MT_per_HA': 'mean',  # Use mean yield
            'Extreme_Weather_Events': 'median',  # Use median for count data
            'Irrigation_Access_%': 'mean',  # Use mean for percentage
            'Pesticide_Use_KG_per_HA': 'mean',  # Use mean for usage
            'Fertilizer_Use_KG_per_HA': 'mean',  # Use mean for usage
            'Soil_Health_Index': 'mean',  # Use mean for index
            'Adaptation_Strategies': 'mode',  # Use most common strategy
            'Economic_Impact_Million_USD': 'mean'  # Use mean for economic impact
        }
            
        for col in columns:
            if col not in df.columns:
                logger.warning(f"src.data_preprocessing.clean_data.handle_missing_values: Column '{col}' not found in DataFrame")
                continue
                
            # Skip if column has no missing values
            if df[col].isna().sum() == 0:
                continue
                
            # Use column-specific strategy if available
            col_strategy = column_strategies.get(col, strategy)
                
            # Handle numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                try:
                    if col_strategy == 'mean':
                        df[col] = df[col].fillna(df[col].mean())
                    elif col_strategy == 'median':
                        df[col] = df[col].fillna(df[col].median())
                    elif col_strategy == 'mode':
                        df[col] = df[col].fillna(df[col].mode()[0])
                    elif col_strategy == 'drop':
                        df = df.dropna(subset=[col])
                    else:
                        logger.warning(f"src.data_preprocessing.clean_data.handle_missing_values: Invalid strategy '{col_strategy}' for numeric column '{col}'. Using 'mean' instead.")
                        df[col] = df[col].fillna(df[col].mean())
                except Exception as e:
                    logger.error(f"src.data_preprocessing.clean_data.handle_missing_values: Error processing numeric column '{col}': {str(e)}")
                    continue
            # Handle categorical columns
            else:
                try:
                    if col_strategy == 'mode':
                        df[col] = df[col].fillna(df[col].mode()[0])
                    elif col_strategy == 'drop':
                        df = df.dropna(subset=[col])
                    else:
                        logger.warning(f"src.data_preprocessing.clean_data.handle_missing_values: Strategy '{col_strategy}' not valid for categorical column '{col}'. Using 'mode' instead.")
                        df[col] = df[col].fillna(df[col].mode()[0])
                except Exception as e:
                    logger.error(f"src.data_preprocessing.clean_data.handle_missing_values: Error processing categorical column '{col}': {str(e)}")
                    continue
                    
        logger.info(f"src.data_preprocessing.clean_data.handle_missing_values: Successfully handled missing values using strategy: {strategy}")
        return df
        
    except Exception as e:
        logger.error(f"src.data_preprocessing.clean_data.handle_missing_values: Error in handle_missing_values: {str(e)}")
        return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the dataset.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe without duplicates
    """
    try:
        if not isinstance(df, pd.DataFrame):
            logger.error("src.data_preprocessing.clean_data.remove_duplicates: Input must be a pandas DataFrame")
            return df
            
        initial_rows = len(df)
        df = df.drop_duplicates()
        removed_rows = initial_rows - len(df)
        
        if removed_rows > 0:
            logger.info(f"src.data_preprocessing.clean_data.remove_duplicates: Removed {removed_rows} duplicate rows")
        else:
            logger.info("src.data_preprocessing.clean_data.remove_duplicates: No duplicate rows found")
            
        return df
        
    except Exception as e:
        logger.error(f"src.data_preprocessing.clean_data.remove_duplicates: Error in remove_duplicates: {str(e)}")
        return df