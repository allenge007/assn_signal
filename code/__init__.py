"""
Environmental Sound Classification System
A modular system for classifying environmental sounds using ESC-50 dataset
with STFT features and CNN models (ResNet, Siamese, Attention).
"""

__version__ = "1.0.0"
__author__ = "Environmental Sound Classification Team"

# Import main modules
from . import data_processing
from . import models
from . import training
from . import utils
from . import config

__all__ = [
    'data_processing',
    'models', 
    'training',
    'utils',
    'config'
]

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = {
        'tensorflow': '2.10.0',
        'librosa': '0.9.0',
        'numpy': '1.21.0',
        'pandas': '1.4.0',
        'sklearn': '1.1.0',
        'matplotlib': '3.5.0',
        'seaborn': '0.11.0'
    }
    
    missing_packages = []
    
    for package, min_version in required_packages.items():
        try:
            if package == 'sklearn':
                import sklearn
                package_name = 'scikit-learn'
            else:
                __import__(package)
                package_name = package
            print(f"✓ {package_name} is installed")
        except ImportError:
            missing_packages.append(package_name)
            print(f"✗ {package_name} is missing")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All required dependencies are installed!")
        return True

def print_system_requirements():
    """Print system requirements information"""
    print("System Requirements:")
    print("- Python 3.8-3.10 (3.9 recommended)")
    print("- Memory: 8GB+ RAM (16GB recommended)")
    print("- Storage: ~2GB for ESC-50 dataset")
    print("- GPU: Optional but recommended")
    print("- ffmpeg: Required for audio processing")
