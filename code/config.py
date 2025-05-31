"""
Configuration settings for the environmental sound classification system.
"""

import os
from dataclasses import dataclass, field
from typing import Tuple, List

@dataclass
class DataConfig:
    """Data processing configuration"""
    dataset_path: str = "./data/ESC-50"
    sample_rate: int = 22050
    duration: float = 5.0  # seconds
    n_fft: int = 2048
    hop_length: int = 512
    n_mels: int = 128
    window: str = "hann"
    
@dataclass 
class ModelConfig:
    """Model configuration"""
    input_shape: Tuple[int, int, int] = (128, 216, 1)  # (n_mels, time_steps, channels)
    num_classes: int = 50
    dropout_rate: float = 0.3
    
@dataclass
class TrainingConfig:
    """Training configuration"""
    batch_size: int = 32
    epochs: int = 100
    learning_rate: float = 0.001
    validation_split: float = 0.2
    early_stopping_patience: int = 10
    save_best_model: bool = True
    model_save_path: str = "./models"
    
@dataclass
class Config:
    """Main configuration class"""
    data: DataConfig = field(default_factory=DataConfig)
    model: ModelConfig = field(default_factory=ModelConfig) 
    training: TrainingConfig = field(default_factory=TrainingConfig)
    
    def __post_init__(self):
        # Create directories if they don't exist
        os.makedirs(self.training.model_save_path, exist_ok=True)
        os.makedirs(os.path.dirname(self.data.dataset_path), exist_ok=True)

# Global config instance
config = Config()
