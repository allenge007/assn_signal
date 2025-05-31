"""
Data processing module for ESC-50 environmental sound classification.
Handles audio loading, STFT computation, and feature extraction.
"""

import os
import pandas as pd
import numpy as np
import librosa
import librosa.display
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from typing import Tuple, List, Optional
import matplotlib.pyplot as plt

from .config import config

class ESC50DataProcessor:
    """ESC-50 dataset processor with STFT feature extraction"""
    
    def __init__(self, dataset_path: str = None):
        self.dataset_path = dataset_path or config.data.dataset_path
        self.sample_rate = config.data.sample_rate
        self.duration = config.data.duration
        self.n_fft = config.data.n_fft
        self.hop_length = config.data.hop_length
        self.n_mels = config.data.n_mels
        self.window = config.data.window
        
        self.label_encoder = LabelEncoder()
        self.metadata = None
        
    def load_metadata(self) -> pd.DataFrame:
        """Load ESC-50 metadata"""
        metadata_path = os.path.join(self.dataset_path, "meta", "esc50.csv")
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        
        self.metadata = pd.read_csv(metadata_path)
        return self.metadata
    
    def load_audio(self, filename: str) -> np.ndarray:
        """Load and preprocess audio file"""
        audio_path = os.path.join(self.dataset_path, "audio", filename)
        
        # Load audio
        audio, sr = librosa.load(audio_path, sr=self.sample_rate, duration=self.duration)
        
        # Pad or trim to fixed length
        target_length = int(self.sample_rate * self.duration)
        if len(audio) < target_length:
            audio = np.pad(audio, (0, target_length - len(audio)), mode='constant')
        else:
            audio = audio[:target_length]
            
        return audio
    
    def compute_stft_features(self, audio: np.ndarray) -> np.ndarray:
        """Compute STFT-based log power spectrogram"""
        # Compute STFT
        stft = librosa.stft(
            audio, 
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            window=self.window
        )
        
        # Convert to log power spectrogram
        magnitude = np.abs(stft)
        log_spectrogram = librosa.amplitude_to_db(magnitude, ref=np.max)
        
        return log_spectrogram
    
    def compute_mel_spectrogram(self, audio: np.ndarray) -> np.ndarray:
        """Compute mel-scale spectrogram"""
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=self.sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=self.n_mels,
            window=self.window
        )
        
        # Convert to log scale
        log_mel_spec = librosa.amplitude_to_db(mel_spec, ref=np.max)
        
        return log_mel_spec
    
    def prepare_dataset(self, feature_type: str = "mel") -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Prepare the complete dataset with features and labels"""
        if self.metadata is None:
            self.load_metadata()
        
        features = []
        labels = []
        
        print(f"Processing {len(self.metadata)} audio files...")
        
        for idx, row in self.metadata.iterrows():
            try:
                # Load audio
                audio = self.load_audio(row['filename'])
                
                # Extract features
                if feature_type == "mel":
                    feature = self.compute_mel_spectrogram(audio)
                elif feature_type == "stft":
                    feature = self.compute_stft_features(audio)
                else:
                    raise ValueError(f"Unknown feature type: {feature_type}")
                
                features.append(feature)
                labels.append(row['category'])
                
                if (idx + 1) % 100 == 0:
                    print(f"Processed {idx + 1}/{len(self.metadata)} files")
                    
            except Exception as e:
                print(f"Error processing {row['filename']}: {e}")
                continue
        
        # Convert to numpy arrays
        features = np.array(features)
        
        # Add channel dimension for CNN
        features = np.expand_dims(features, axis=-1)
        
        # Encode labels
        labels_encoded = self.label_encoder.fit_transform(labels)
        
        # Get class names
        class_names = self.label_encoder.classes_.tolist()
        
        print(f"Dataset prepared: {features.shape}, {len(np.unique(labels_encoded))} classes")
        
        return features, labels_encoded, class_names
    
    def create_train_val_split(self, features: np.ndarray, labels: np.ndarray, 
                              test_size: float = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Create train/validation split"""
        test_size = test_size or config.training.validation_split
        
        return train_test_split(
            features, labels, 
            test_size=test_size, 
            random_state=42, 
            stratify=labels
        )
    
    def visualize_spectrogram(self, audio: np.ndarray, feature_type: str = "mel", 
                            save_path: str = None):
        """Visualize spectrogram"""
        plt.figure(figsize=(12, 6))
        
        if feature_type == "mel":
            feature = self.compute_mel_spectrogram(audio)
            librosa.display.specshow(
                feature, 
                sr=self.sample_rate,
                hop_length=self.hop_length,
                x_axis='time',
                y_axis='mel'
            )
            plt.title('Mel Spectrogram')
        elif feature_type == "stft":
            feature = self.compute_stft_features(audio)
            librosa.display.specshow(
                feature,
                sr=self.sample_rate, 
                hop_length=self.hop_length,
                x_axis='time',
                y_axis='hz'
            )
            plt.title('STFT Spectrogram')
        
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.show()

def create_tensorflow_dataset(X: np.ndarray, y: np.ndarray, batch_size: int = None, 
                            shuffle: bool = True) -> tf.data.Dataset:
    """Create TensorFlow dataset from numpy arrays"""
    batch_size = batch_size or config.training.batch_size
    
    dataset = tf.data.Dataset.from_tensor_slices((X, y))
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=1000)
    
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    
    return dataset
