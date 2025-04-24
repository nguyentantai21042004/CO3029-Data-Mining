"""
Module for splitting data into training and testing sets.
"""
import pandas as pd #type: ignore
import numpy as np #type: ignore
from typing import Tuple #type: ignore
from sklearn.model_selection import train_test_split #type: ignore
from utils.logging import logger

def split_train_test(df: pd.DataFrame, 
                    target_column: str,
                    test_size: float = 0.2,
                    random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split data into training and testing sets.
    
    Args:
        df (pd.DataFrame): Input dataframe
        target_column (str): Name of the target column
        test_size (float): Proportion of the dataset to include in the test split
        random_state (int): Random seed for reproducibility
        
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: X_train, X_test, y_train, y_test
    """
    try:
        if not isinstance(df, pd.DataFrame):
            logger.error("src.data_preprocessing.split_data.split_train_test: Input must be a pandas DataFrame")
            return None, None, None, None
            
        if target_column not in df.columns:
            logger.error(f"src.data_preprocessing.split_data.split_train_test: Target column '{target_column}' not found in DataFrame")
            return None, None, None, None
            
        if not 0 < test_size < 1:
            logger.error(f"src.data_preprocessing.split_data.split_train_test: Invalid test_size {test_size}. Must be between 0 and 1")
            return None, None, None, None
            
        logger.info(f"src.data_preprocessing.split_data.split_train_test: Splitting data with test_size={test_size}, random_state={random_state}")
        
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        logger.info(f"src.data_preprocessing.split_data.split_train_test: Successfully split data. Train shape: {X_train.shape}, Test shape: {X_test.shape}")
        return X_train, X_test, y_train, y_test
        
    except Exception as e:
        logger.error(f"src.data_preprocessing.split_data.split_train_test: Error splitting data: {str(e)}")
        return None, None, None, None