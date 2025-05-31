"""
Training module for environmental sound classification models.
Handles model training, evaluation, and saving.
"""

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import time

from .config import config
from .models import get_model
from .data_processing import ESC50DataProcessor

class ModelTrainer:
    """Model training and evaluation class"""
    
    def __init__(self, model_type: str = "resnet"):
        self.model_type = model_type
        self.model = None
        self.history = None
        self.class_names = None
        
    def prepare_model(self, num_classes: int, input_shape: Tuple[int, int, int] = None):
        """Prepare model for training"""
        input_shape = input_shape or config.model.input_shape
        
        self.model = get_model(
            model_type=self.model_type,
            input_shape=input_shape,
            num_classes=num_classes
        )
        
        # Compile model
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=config.training.learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"Model '{self.model_type}' prepared with {self.model.count_params()} parameters")
        return self.model
    
    def create_callbacks(self, model_name: str = None) -> List[keras.callbacks.Callback]:
        """Create training callbacks"""
        model_name = model_name or f"{self.model_type}_{int(time.time())}"
        model_path = os.path.join(config.training.model_save_path, f"{model_name}.h5")
        
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=config.training.early_stopping_patience,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        if config.training.save_best_model:
            callbacks.append(
                ModelCheckpoint(
                    filepath=model_path,
                    monitor='val_accuracy',
                    save_best_only=True,
                    save_weights_only=False,
                    verbose=1
                )
            )
        
        return callbacks
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              X_val: np.ndarray, y_val: np.ndarray,
              class_names: List[str] = None,
              model_name: str = None) -> keras.callbacks.History:
        """Train the model"""
        
        if self.model is None:
            self.prepare_model(num_classes=len(np.unique(y_train)), input_shape=X_train.shape[1:])
        
        self.class_names = class_names
        
        # Create callbacks
        callbacks = self.create_callbacks(model_name)
        
        print(f"Training {self.model_type} model...")
        print(f"Training data: {X_train.shape}, Validation data: {X_val.shape}")
        
        # Train model
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=config.training.epochs,
            batch_size=config.training.batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        return self.history
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Evaluate model on test data"""
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        # Make predictions
        y_pred_proba = self.model.predict(X_test)
        y_pred = np.argmax(y_pred_proba, axis=1)
        
        # Calculate metrics
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
        # Classification report
        if self.class_names:
            report = classification_report(
                y_test, y_pred, 
                target_names=self.class_names,
                output_dict=True
            )
        else:
            report = classification_report(y_test, y_pred, output_dict=True)
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        results = {
            'test_loss': test_loss,
            'test_accuracy': test_accuracy,
            'classification_report': report,
            'confusion_matrix': cm,
            'predictions': y_pred,
            'prediction_probabilities': y_pred_proba
        }
        
        print(f"Test Accuracy: {test_accuracy:.4f}")
        print(f"Test Loss: {test_loss:.4f}")
        
        return results
    
    def plot_training_history(self, save_path: str = None):
        """Plot training history"""
        if self.history is None:
            raise ValueError("No training history available!")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot accuracy
        ax1.plot(self.history.history['accuracy'], label='Training Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Plot loss
        ax2.plot(self.history.history['loss'], label='Training Loss')
        ax2.plot(self.history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.show()
    
    def plot_confusion_matrix(self, confusion_matrix: np.ndarray, 
                            class_names: List[str] = None,
                            save_path: str = None):
        """Plot confusion matrix"""
        plt.figure(figsize=(12, 10))
        
        if class_names and len(class_names) <= 20:  # Only show labels if not too many
            sns.heatmap(
                confusion_matrix, 
                annot=True, 
                fmt='d', 
                cmap='Blues',
                xticklabels=class_names,
                yticklabels=class_names
            )
        else:
            sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues')
        
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.show()
    
    def save_model(self, filepath: str):
        """Save trained model"""
        if self.model is None:
            raise ValueError("No model to save!")
        
        self.model.save(filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model"""
        self.model = keras.models.load_model(filepath)
        print(f"Model loaded from {filepath}")

def train_all_models(X_train: np.ndarray, y_train: np.ndarray,
                    X_val: np.ndarray, y_val: np.ndarray,
                    X_test: np.ndarray, y_test: np.ndarray,
                    class_names: List[str] = None) -> Dict:
    """Train and evaluate all model types"""
    
    model_types = ["simple_cnn", "resnet", "attention", "siamese"]
    results = {}
    
    for model_type in model_types:
        print(f"\n{'='*50}")
        print(f"Training {model_type.upper()} model")
        print(f"{'='*50}")
        
        # Create trainer
        trainer = ModelTrainer(model_type=model_type)
        
        # Train model
        history = trainer.train(
            X_train, y_train, X_val, y_val,
            class_names=class_names,
            model_name=f"esc50_{model_type}"
        )
        
        # Evaluate model
        eval_results = trainer.evaluate(X_test, y_test)
        
        # Save results
        results[model_type] = {
            'trainer': trainer,
            'history': history,
            'evaluation': eval_results
        }
        
        # Plot training history
        trainer.plot_training_history(
            save_path=f"./plots/{model_type}_training_history.png"
        )
        
        print(f"{model_type.upper()} - Test Accuracy: {eval_results['test_accuracy']:.4f}")
    
    return results

def compare_models(results: Dict):
    """Compare performance of different models"""
    model_names = list(results.keys())
    accuracies = [results[name]['evaluation']['test_accuracy'] for name in model_names]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(model_names, accuracies)
    plt.title('Model Performance Comparison')
    plt.xlabel('Model Type')
    plt.ylabel('Test Accuracy')
    plt.ylim(0, 1)
    
    # Add value labels on bars
    for bar, acc in zip(bars, accuracies):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{acc:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    # Print detailed comparison
    print("\nModel Performance Summary:")
    print("-" * 40)
    for name in model_names:
        acc = results[name]['evaluation']['test_accuracy']
        loss = results[name]['evaluation']['test_loss']
        print(f"{name.upper():12} - Accuracy: {acc:.4f}, Loss: {loss:.4f}")
