"""
Main execution script for ESC-50 environmental sound classification.
This script demonstrates the complete pipeline from data processing to model evaluation.
"""

from datetime import datetime
import config
import os
import sys
import argparse
import numpy as np
from typing import Dict, Any

def main(args: argparse.Namespace):
    """Main execution function"""
    
    # Setup
    print("="*60)
    print("ESC-50 Environmental Sound Classification System")
    print("="*60)
    
    try:
        # Import our modules (moved inside try block for better error handling)
        from .config import config
        from .data_processing import ESC50DataProcessor
        from .training import ModelTrainer, train_all_models, compare_models
        from .utils import (
            download_esc50_dataset, 
            create_project_directories,
            save_results,
            print_system_info,
            ensure_reproducibility,
            Timer
        )
        
        # Print system info
        print_system_info()
        
        # Ensure reproducibility
        ensure_reproducibility(args.seed)
        
        # Create project directories
        create_project_directories()
        
        # Download dataset if needed
        if args.download_dataset:
            dataset_path = download_esc50_dataset(args.data_path)
            config.data.dataset_path = dataset_path
        
        # Initialize data processor
        processor = ESC50DataProcessor(config.data.dataset_path)
        
        # Load and process data
        print("\nLoading ESC-50 dataset...")
        with Timer("Data loading and preprocessing"):
            features, labels, class_names = processor.prepare_dataset(
                feature_type=args.feature_type
            )
        
        print(f"Dataset shape: {features.shape}")
        print(f"Number of classes: {len(class_names)}")
        print(f"Classes: {class_names[:10]}..." if len(class_names) > 10 else f"Classes: {class_names}")
        
        # Create train/validation/test splits
        print("\nCreating data splits...")
        X_train, X_val, y_train, y_val = processor.create_train_val_split(
            features, labels, test_size=0.2
        )
        
        # Further split validation into val and test
        X_val, X_test, y_val, y_test = processor.create_train_val_split(
            X_val, y_val, test_size=0.5
        )
        
        print(f"Train set: {X_train.shape}")
        print(f"Validation set: {X_val.shape}")
        print(f"Test set: {X_test.shape}")
        
        # Update config with actual input shape
        config.model.input_shape = X_train.shape[1:]
        config.model.num_classes = len(class_names)
        
        current_time = datetime.now().strftime("%m-%d_%H-%M")
        # Train models
        if args.model_type == "all":
            save_path = f"./plots-{current_time}"
            print("\nTraining all models...")
            with Timer("Training all models"):
                results = train_all_models(
                    X_train, y_train, X_val, y_val, X_test, y_test,
                    class_names=class_names,
                    save_path=save_path,
                )
            
            # Compare models
            print("\nComparing model performances...")
            
            compare_models(results, f"{save_path}/all_models_results.png")
            
            # Save results
            save_results(results, f"./results-{current_time}/all_models_results.json")
            
        else:
            print(f"\nTraining {args.model_type} model...")
            
            trainer = ModelTrainer(model_type=args.model_type)
            
            with Timer(f"Training {args.model_type}"):
                history = trainer.train(
                    X_train, y_train, X_val, y_val,
                    class_names=class_names,
                    model_name=f"esc50_{args.model_type}"
                )
            
            # Evaluate
            print(f"\nEvaluating {args.model_type} model...")
            eval_results = trainer.evaluate(X_test, y_test)
            
            # Plot results
            trainer.plot_training_history(
                save_path=f"./plots-{current_time}-{args.model_type}/{args.model_type}_training_history.png"
            )
            
            trainer.plot_confusion_matrix(
                eval_results['confusion_matrix'],
                class_names=class_names,
                save_path=f"./plots-{current_time}-{args.model_type}/{args.model_type}_confusion_matrix.png"
            )
            
            # Save single model results
            results = {args.model_type: {'evaluation': eval_results}}
            save_results(results, f"./results-{current_time}-{args.model_type}/{args.model_type}_results.json")
        
        print("\nTraining completed successfully!")
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Please make sure all dependencies are installed. Run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        print("An unexpected error occurred. Please check your setup and try again.")
        sys.exit(1)

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        description="ESC-50 Environmental Sound Classification"
    )
    
    parser.add_argument(
        "--model_type", 
        type=str, 
        default="resnet",
        choices=["resnet", "attention", "siamese", "simple_cnn", "all"],
        help="Type of model to train"
    )
    
    parser.add_argument(
        "--feature_type",
        type=str,
        default="mel",
        choices=["mel", "stft"],
        help="Type of spectral features to extract"
    )
    
    parser.add_argument(
        "--data_path",
        type=str,
        default="./data",
        help="Path to store/find ESC-50 dataset"
    )
    
    parser.add_argument(
        "--download_dataset",
        action="store_true",
        help="Download ESC-50 dataset if not present"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility"
    )
    
    parser.add_argument(
        "--epochs",
        type=int,
        default=None,
        help="Number of training epochs (overrides config)"
    )
    
    parser.add_argument(
        "--batch_size",
        type=int,
        default=None,
        help="Batch size (overrides config)"
    )
    
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=None,
        help="Learning rate (overrides config)"
    )
    
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    
    # Override config with command line arguments if provided
    if args.epochs:
        config.training.epochs = args.epochs
    if args.batch_size:
        config.training.batch_size = args.batch_size
    if args.learning_rate:
        config.training.learning_rate = args.learning_rate
    
    main(args)
