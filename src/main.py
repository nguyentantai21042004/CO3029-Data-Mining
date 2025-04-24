"""
Main script for data preprocessing pipeline.
"""
import os
from typing import List
import pandas as pd
from data_preprocessing.load_data import load_csv, load_excel
from data_preprocessing.clean_data import handle_missing_values, remove_duplicates
from data_preprocessing.feature_engineering import normalize_features, create_dummy_variables, process_numeric_columns
from utils.logging import logger
from utils.configs import config 

def process_file(file_path: str) -> None:
    """
    Process a single data file through the preprocessing pipeline.
    
    Args:
        file_path (str): Path to the data file
    """
    try:
        # Load data
        logger.info(f"Processing file: {file_path}")
        if file_path.endswith('.csv'):
            df = load_csv(file_path)
        else:
            df = load_excel(file_path)
            
        # Log initial data info
        logger.info(f"Initial data shape: {df.shape}")
        logger.info(f"Initial missing values:\n{df.isnull().sum()}")
        
        # Clean data
        df = handle_missing_values(df)
        df = remove_duplicates(df)
        logger.info(f"Data shape after cleaning: {df.shape}")
        logger.info(f"Missing values after cleaning:\n{df.isnull().sum()}")
        
        # Feature engineering
        # 1. Process numeric columns (handle outliers)
        numeric_exclude = ['Year', 'Year Code', 'Area Code', 'Element Code', 'Item Code']
        df = process_numeric_columns(df, exclude_columns=numeric_exclude)
        
        # 2. Normalize numeric columns
        df = normalize_features(df, exclude_columns=numeric_exclude)
        
        # 3. Create dummy variables for categorical columns
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        df = create_dummy_variables(df, columns=categorical_columns, max_categories=10, keep_original=False)
        
        # Log final data info
        logger.info(f"Final data shape: {df.shape}")
        logger.info(f"Final data types:\n{df.dtypes}")
        
        # Save processed data
        output_file = os.path.join(config.PROCESSED_DATA_PATH, f"processed_{os.path.basename(file_path)}")
        df.to_csv(output_file, index=False)
        logger.info(f"Processed data saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")

def main():
    """
    Main function to run the data preprocessing pipeline.
    """
    try:
        # Create processed data directory if it doesn't exist
        os.makedirs(config.PROCESSED_DATA_PATH, exist_ok=True)
        
        # Get list of data files
        data_files = [os.path.join(config.RAW_DATA_PATH, f) for f in os.listdir(config.RAW_DATA_PATH) 
                     if f.endswith(('.csv', '.xlsx', '.xls'))]
        
        logger.info(f"Found {len(data_files)} data files to process")
        
        # Process each file
        for file_path in data_files:
            process_file(file_path)
            
        logger.info("Data preprocessing completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main() 