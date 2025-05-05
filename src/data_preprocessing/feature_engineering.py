"""
Module for feature engineering and transformation.
"""
import pandas as pd #type: ignore
import numpy as np #type: ignore
from typing import List, Optional #type: ignore
from sklearn.preprocessing import MinMaxScaler #type: ignore
from utils.logging import logger

def normalize_features(df: pd.DataFrame, 
                      columns: Optional[List[str]] = None,
                      exclude_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Normalize features in the dataset using MinMaxScaler.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (List[str], optional): Columns to normalize
        exclude_columns (List[str], optional): Columns to exclude from normalization
        
    Returns:
        pd.DataFrame: Dataframe with normalized features
    """
    try:
        if not isinstance(df, pd.DataFrame):
            logger.error("Input must be a pandas DataFrame")
            return df
            
        df = df.copy()
        
        # Get numeric columns if not specified
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
        # Exclude specified columns
        if exclude_columns:
            columns = [col for col in columns if col not in exclude_columns]
            
        # Check if columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            logger.warning(f"Columns not found: {missing_cols}")
            columns = [col for col in columns if col in df.columns]
        
        if not columns:
            logger.warning("No valid columns to normalize")
            return df
            
        # Initialize MinMaxScaler
        scaler = MinMaxScaler()
            
        # Normalize features
        df[columns] = scaler.fit_transform(df[columns])
        logger.info(f"Successfully normalized {len(columns)} columns using MinMaxScaler")
        return df
        
    except Exception as e:
        logger.error(f"Error in normalize_features: {str(e)}")
        return df

def create_dummy_variables(df: pd.DataFrame, 
                         columns: Optional[List[str]] = None,
                         max_categories: int = 10,
                         keep_original: bool = False) -> pd.DataFrame:
    """
    Create dummy variables for categorical features with category limits.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (List[str], optional): Columns to create dummies for
        max_categories (int): Maximum number of categories to create dummies for
        keep_original (bool): Whether to keep the original categorical columns
        
    Returns:
        pd.DataFrame: Dataframe with dummy variables
    """
    try:
        if not isinstance(df, pd.DataFrame):
            logger.error("Input must be a pandas DataFrame")
            return df
            
        df = df.copy()
        
        # Get categorical columns if not specified
        if columns is None:
            columns = ['Country', 'Region', 'Crop_Type', 'Adaptation_Strategies']
            
        # Check if columns exist
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            logger.warning(f"Columns not found: {missing_cols}")
            columns = [col for col in columns if col in df.columns]
        
        if not columns:
            logger.warning("No valid columns to create dummies for")
            return df
            
        # Create dummy variables with category limit
        for col in columns:
            # Skip if column is numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                logger.info(f"Skipping numeric column: {col}")
                continue
                
            # Get value counts
            value_counts = df[col].value_counts()
            
            # If number of categories exceeds max_categories, keep only top categories
            if len(value_counts) > max_categories:
                top_categories = value_counts.nlargest(max_categories-1).index
                df[col] = df[col].where(df[col].isin(top_categories), 'Other')
                
            # Create dummies
            dummies = pd.get_dummies(df[col], prefix=col)
            
            # Add 'Other' category if it doesn't exist
            if 'Other' not in df[col].unique() and len(value_counts) > max_categories:
                dummies[f"{col}_Other"] = False
                
            # Concatenate dummies
            df = pd.concat([df, dummies], axis=1)
            
            # Drop original column if not keeping it
            if not keep_original:
                df = df.drop(columns=[col])
            
        logger.info(f"Successfully created dummy variables for {len(columns)} columns")
        return df
        
    except Exception as e:
        logger.error(f"Error in create_dummy_variables: {str(e)}")
        return df

def process_numeric_columns(df: pd.DataFrame, 
                          exclude_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Process numeric columns by handling outliers and normalizing.
    
    Args:
        df (pd.DataFrame): Input dataframe
        exclude_columns (List[str], optional): Columns to exclude from processing
        
    Returns:
        pd.DataFrame: Processed dataframe
    """
    try:
        if not isinstance(df, pd.DataFrame):
            logger.error("Input must be a pandas DataFrame")
            return df
            
        df = df.copy()
        
        # Define columns to process and their specific treatments
        numeric_columns = {
            'Year': {'method': 'clip', 'min': 1990, 'max': 2024},  # Clip to valid year range
            'Average_Temperature_C': {'method': 'iqr'},  # Use IQR method
            'Total_Precipitation_mm': {'method': 'iqr'},  # Use IQR method
            'CO2_Emissions_MT': {'method': 'iqr'},  # Use IQR method
            'Crop_Yield_MT_per_HA': {'method': 'iqr'},  # Use IQR method
            'Extreme_Weather_Events': {'method': 'clip', 'min': 0, 'max': 10},  # Clip to reasonable range
            'Irrigation_Access_%': {'method': 'clip', 'min': 0, 'max': 100},  # Clip to percentage range
            'Pesticide_Use_KG_per_HA': {'method': 'iqr'},  # Use IQR method
            'Fertilizer_Use_KG_per_HA': {'method': 'iqr'},  # Use IQR method
            'Soil_Health_Index': {'method': 'clip', 'min': 0, 'max': 100},  # Clip to index range
            'Economic_Impact_Million_USD': {'method': 'iqr'}  # Use IQR method
        }
        
        # Exclude specified columns
        if exclude_columns:
            numeric_columns = {k: v for k, v in numeric_columns.items() if k not in exclude_columns}
            
        for col, treatment in numeric_columns.items():
            if col not in df.columns:
                continue
                
            if treatment['method'] == 'iqr':
                # Handle outliers using IQR method
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Replace outliers with bounds
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
                
            elif treatment['method'] == 'clip':
                # Clip values to specified range
                df[col] = df[col].clip(lower=treatment['min'], upper=treatment['max'])
            
        logger.info(f"Successfully processed numeric columns")
        return df
        
    except Exception as e:
        logger.error(f"Error in process_numeric_columns: {str(e)}")
        return df