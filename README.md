# Data Mining Project - Crop Yield Analysis

## Project Overview
This project focuses on analyzing crop yield data and its relationship with various environmental and agricultural factors. The analysis includes data preprocessing, feature engineering, and predictive modeling to understand the impact of different variables on crop yields.

## Data Sources
The project uses multiple datasets:
1. `yield.csv`: Crop yield data from FAO
2. `temp.csv`: Temperature data
3. `pesticides.csv`: Pesticide usage data
4. `rainfall.csv`: Rainfall data
5. `yield_df.csv`: Combined dataset with yield, rainfall, temperature, and pesticide data

## Data Preprocessing Pipeline

### 1. Data Loading
- **Automatic Type Detection**: The system automatically detects and converts numeric columns based on:
  - Column names (containing keywords like 'value', 'avg', 'average', 'temp', 'rain', 'yield', 'tonnes')
  - Column values (if all values can be converted to numeric)
- **Support for Multiple Formats**: Handles both CSV and Excel files
- **Smart Date Handling**: Automatic conversion of date columns

### 2. Data Cleaning
- **Missing Value Handling**:
  - Numeric columns: Filled with mean values
  - Categorical columns: Filled with mode values
- **Duplicate Removal**: Automatic detection and removal of duplicate rows
- **Data Validation**: Checks for data type consistency and missing values

### 3. Feature Engineering
- **Numeric Column Processing**:
  - Outlier detection and handling using IQR method
  - Normalization using MinMaxScaler
  - Automatic identification of numeric columns
- **Categorical Column Processing**:
  - One-hot encoding with category limits
  - Maximum of 10 categories per feature (top categories + 'Other')
  - Option to keep original categorical columns
- **Smart Column Selection**:
  - Automatic exclusion of specific columns (e.g., Year, Year Code, Area Code)
  - Type-based column selection for different processing steps

### 4. Data Quality Checks
- **Shape Validation**: Ensures data dimensions are maintained
- **Type Verification**: Confirms correct data types after processing
- **Missing Value Verification**: Ensures all missing values are handled
- **Logging**: Detailed logging of all processing steps and changes

## Project Structure
```
.
├── data/
│   ├── raw/              # Original data files
│   └── processed/        # Processed data files
├── src/
│   ├── data_preprocessing/
│   │   ├── load_data.py      # Data loading functions
│   │   ├── clean_data.py     # Data cleaning functions
│   │   └── feature_engineering.py  # Feature engineering functions
│   ├── utils/
│   │   ├── logging.py        # Logging configuration
│   │   └── config.py         # Configuration settings
│   └── main.py              # Main processing script
└── README.md
```

## Usage
1. Place raw data files in `data/raw/` directory
2. Run the preprocessing pipeline:
   ```bash
   python src/main.py
   ```
3. Processed files will be saved in `data/processed/` directory

## Key Features
- **Automated Processing**: Minimal manual intervention required
- **Robust Error Handling**: Graceful handling of various data issues
- **Detailed Logging**: Comprehensive logging of all processing steps
- **Flexible Configuration**: Easy to modify processing parameters
- **Type Safety**: Strong type checking and conversion
- **Scalability**: Can handle large datasets efficiently

## Data Processing Results
Each dataset undergoes the following transformations:

### yield.csv
- Original: 56,717 rows × 12 columns
- Processed: 56,717 rows × 30 columns
- Features: Numeric columns normalized, categorical columns one-hot encoded

### temp.csv
- Original: 71,311 rows × 3 columns
- Processed: 64,353 rows × 12 columns
- Features: Temperature data normalized, country names one-hot encoded

### pesticides.csv
- Original: 4,349 rows × 7 columns
- Processed: 4,349 rows × 16 columns
- Features: Usage data normalized, categorical variables encoded

### rainfall.csv
- Original: 6,727 rows × 3 columns
- Processed: 6,727 rows × 12 columns
- Features: Rainfall data normalized, area names encoded

### yield_df.csv
- Original: 28,242 rows × 8 columns
- Processed: 28,242 rows × 26 columns
- Features: All numeric columns normalized, categorical variables encoded

## Next Steps
1. Exploratory Data Analysis (EDA)
2. Feature Selection
3. Model Development
4. Model Evaluation
5. Results Interpretation

## Requirements
- Python 3.8+
- pandas
- numpy
- scikit-learn
- logging
- typing
