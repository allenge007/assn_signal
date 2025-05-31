"""
Utility functions for the environmental sound classification system.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from typing import Dict, List, Any, Optional
import zipfile
import requests
from tqdm import tqdm

def download_esc50_dataset(save_path: str = "./data") -> str:
    """Download ESC-50 dataset if not already present"""
    dataset_url = "https://github.com/karolpiczak/ESC-50/archive/master.zip"
    dataset_path = os.path.join(save_path, "ESC-50")
    
    if os.path.exists(dataset_path):
        print(f"ESC-50 dataset already exists at {dataset_path}")
        return dataset_path
    
    os.makedirs(save_path, exist_ok=True)
    zip_path = os.path.join(save_path, "esc50.zip")
    
    print("Downloading ESC-50 dataset...")
    
    # Download with progress bar
    response = requests.get(dataset_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(zip_path, 'wb') as file, tqdm(
        desc="Downloading",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                pbar.update(len(chunk))
    
    print("Extracting dataset...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(save_path)
    
    # Rename extracted folder
    extracted_path = os.path.join(save_path, "ESC-50-master")
    if os.path.exists(extracted_path):
        os.rename(extracted_path, dataset_path)
    
    # Clean up zip file
    os.remove(zip_path)
    
    print(f"ESC-50 dataset downloaded and extracted to {dataset_path}")
    return dataset_path

def save_results(results: Dict, filepath: str):
    """Save experiment results to JSON"""
    # Convert numpy arrays to lists for JSON serialization
    serializable_results = {}
    
    for model_name, model_results in results.items():
        serializable_results[model_name] = {
            'test_accuracy': float(model_results['evaluation']['test_accuracy']),
            'test_loss': float(model_results['evaluation']['test_loss']),
            'classification_report': model_results['evaluation']['classification_report']
        }
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"Results saved to {filepath}")

def load_results(filepath: str) -> Dict:
    """Load experiment results from JSON"""
    with open(filepath, 'r') as f:
        results = json.load(f)
    return results

def create_project_directories():
    """Create necessary project directories"""
    directories = [
        "./data",
        "./models", 
        "./results",
        "./plots",
        "./logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Project directories created")

def plot_audio_waveform(audio: np.ndarray, sr: int = 22050, 
                       title: str = "Audio Waveform", save_path: str = None):
    """Plot audio waveform"""
    plt.figure(figsize=(12, 4))
    
    time_axis = np.linspace(0, len(audio) / sr, len(audio))
    plt.plot(time_axis, audio)
    plt.title(title)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_spectrogram_comparison(audio: np.ndarray, sr: int = 22050,
                              save_path: str = None):
    """Plot comparison of different spectrogram types"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # STFT
    stft = librosa.stft(audio)
    stft_db = librosa.amplitude_to_db(np.abs(stft))
    librosa.display.specshow(stft_db, sr=sr, x_axis='time', y_axis='hz', ax=axes[0,0])
    axes[0,0].set_title('STFT Spectrogram')
    
    # Mel spectrogram
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr)
    mel_spec_db = librosa.amplitude_to_db(mel_spec)
    librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel', ax=axes[0,1])
    axes[0,1].set_title('Mel Spectrogram')
    
    # Chromagram
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
    librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma', ax=axes[1,0])
    axes[1,0].set_title('Chromagram')
    
    # Spectral centroid
    spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
    time_axis = np.linspace(0, len(audio)/sr, len(spectral_centroids))
    axes[1,1].plot(time_axis, spectral_centroids)
    axes[1,1].set_title('Spectral Centroid')
    axes[1,1].set_xlabel('Time (s)')
    axes[1,1].set_ylabel('Hz')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def get_system_info() -> Dict[str, Any]:
    """Get system information for reproducibility"""
    import tensorflow as tf
    import platform
    
    info = {
        'python_version': platform.python_version(),
        'tensorflow_version': tf.__version__,
        'platform': platform.platform(),
        'gpu_available': tf.config.list_physical_devices('GPU') != []
    }
    
    if info['gpu_available']:
        gpu_devices = tf.config.list_physical_devices('GPU')
        info['gpu_devices'] = [device.name for device in gpu_devices]
    
    return info

def print_system_info():
    """Print system information"""
    info = get_system_info()
    
    print("System Information:")
    print("-" * 30)
    for key, value in info.items():
        print(f"{key}: {value}")

class Timer:
    """Simple timer context manager"""
    
    def __init__(self, description: str = "Operation"):
        self.description = description
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        print(f"Starting {self.description}...")
        return self
        
    def __exit__(self, *args):
        elapsed_time = time.time() - self.start_time
        print(f"{self.description} completed in {elapsed_time:.2f} seconds")

def ensure_reproducibility(seed: int = 42):
    """Ensure reproducible results"""
    np.random.seed(seed)
    tf.random.set_seed(seed)
    
    # Set deterministic operations
    os.environ['TF_DETERMINISTIC_OPS'] = '1'
    tf.config.experimental.enable_op_determinism()
    
    print(f"Random seed set to {seed} for reproducibility")
