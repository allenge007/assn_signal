# Environmental Sound Classification System

A modular system for classifying environmental sounds using the ESC-50 dataset with STFT features and CNN models (ResNet, Siamese-like networks, and Attention mechanisms).

## Features

- **Multiple Model Architectures**: ResNet, Siamese-like networks, Attention mechanisms, and simple CNN
- **Advanced Audio Processing**: STFT and Mel-spectrogram feature extraction
- **Modular Design**: Separate modules for data processing, model training, and evaluation
- **Comprehensive Evaluation**: Training curves, confusion matrices, and performance comparisons
- **Reproducible Results**: Seed management and configuration system

## Environment Setup

### Option 1: Using Conda (Recommended)

```bash
# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate esc50_classification
```

### Option 2: Using pip and virtualenv

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 3: Using pip directly

```bash
# Install dependencies directly
pip install -r requirements.txt
```

## System Requirements

- **Python**: 3.8-3.10 (3.9 recommended)
- **Memory**: At least 8GB RAM (16GB recommended)
- **Storage**: ~2GB for ESC-50 dataset
- **GPU**: Optional but recommended for faster training

### Additional System Dependencies

#### For audio processing (ffmpeg):

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## Quick Start

1. **Setup environment** (see above)

2. **Run the system:**
```bash
# Train all models with automatic dataset download
python -m code.main --model_type all --download_dataset

# Train specific model
python -m code.main --model_type resnet --feature_type mel

# Custom training parameters
python -m code.main --model_type attention --epochs 50 --batch_size 64 --learning_rate 0.0005
```

3. **Available model types:**
   - `resnet`: ResNet-based architecture
   - `attention`: CNN with self-attention mechanism
   - `siamese`: Siamese-like network
   - `simple_cnn`: Baseline CNN model
   - `all`: Train and compare all models

## Project Structure

```
assn_signal/
├── code/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── data_processing.py   # ESC-50 data loading and preprocessing
│   ├── models.py            # Model architectures
│   ├── training.py          # Training and evaluation pipeline
│   ├── utils.py             # Utility functions
│   └── main.py              # Main execution script
├── data/                    # Dataset storage (auto-created)
├── models/                  # Saved models (auto-created)
├── results/                 # Experiment results (auto-created)
├── plots/                   # Generated plots (auto-created)
├── requirements.txt         # Python dependencies
├── environment.yml          # Conda environment
└── README.md               # This file
```

## Usage Examples

### Basic Usage
```python
from code.data_processing import ESC50DataProcessor
from code.training import ModelTrainer

# Process data
processor = ESC50DataProcessor()
features, labels, class_names = processor.prepare_dataset()

# Train model
trainer = ModelTrainer(model_type="resnet")
trainer.prepare_model(num_classes=50)
# ... training code
```

### Configuration
```python
from code.config import config

# Modify configuration
config.training.epochs = 100
config.training.batch_size = 64
config.data.sample_rate = 22050
```

## Results

The system will generate:
- Training/validation curves
- Confusion matrices
- Performance comparison charts
- Model evaluation reports
- Saved trained models

## Troubleshooting

### Common Issues

1. **Audio loading errors**: Ensure ffmpeg is properly installed
2. **Memory issues**: Reduce batch_size in config or use a machine with more RAM
3. **GPU not detected**: Install tensorflow-gpu or ensure CUDA is properly configured
4. **Dataset download fails**: Check internet connection or manually download ESC-50

### Performance Tips

- Use GPU for faster training
- Increase batch_size if you have sufficient memory
- Use mel spectrograms for faster processing
- Enable mixed precision training for large models

## Citation

If you use this code in your research, please cite the ESC-50 dataset:

```
Piczak, K. J. (2015). ESC: Dataset for Environmental Sound Classification. 
Proceedings of the 23rd ACM international conference on Multimedia (pp. 1015-1018).
```