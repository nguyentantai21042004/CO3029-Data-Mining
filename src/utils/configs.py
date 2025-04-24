"""
Configuration settings for the project.
"""
from dataclasses import dataclass, field
from typing import Dict, Any
import os

@dataclass
class Config:
    # Data paths (relative to project root)
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    RAW_DATA_PATH: str = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_PATH: str = os.path.join(DATA_DIR, 'processed')
    
    # Model parameters
    DEFAULT_MODEL_PARAMS: Dict[str, Any] = field(default_factory=lambda: {
        'random_state': 42,
        'test_size': 0.2,
        'cv_folds': 5
    })
    
    # Feature engineering parameters
    FEATURE_PARAMS: Dict[str, Any] = field(default_factory=lambda: {
        'normalization_method': 'standard',
        'missing_value_strategy': 'mean'
    })
    
    # Plotting parameters
    PLOT_PARAMS: Dict[str, Any] = field(default_factory=lambda: {
        'figure_size': (10, 6),
        'font_size': 12,
        'color_palette': 'viridis'
    })
    
    # Preprocessing parameters
    PREPROCESSING_CONFIG: Dict[str, Any] = field(default_factory=lambda: {
        'missing_value_strategy': 'mean',
        'normalization_method': 'standard',
        'categorical_handling': 'one_hot'
    })

# Create a global config instance
config = Config()
