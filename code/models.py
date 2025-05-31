"""
Model definitions for environmental sound classification.
Includes ResNet, Siamese-like networks, and attention mechanisms.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from typing import Tuple, Optional
import numpy as np

from .config import config

class AttentionBlock(layers.Layer):
    """Self-attention mechanism for spectrograms"""
    
    def __init__(self, units: int, **kwargs):
        super(AttentionBlock, self).__init__(**kwargs)
        self.units = units
        self.W_q = layers.Dense(units)
        self.W_k = layers.Dense(units)
        self.W_v = layers.Dense(units)
        self.softmax = layers.Softmax(axis=-1)
        
    def call(self, inputs):
        # inputs shape: (batch_size, height, width, channels)
        batch_size = tf.shape(inputs)[0]
        height = tf.shape(inputs)[1]
        width = tf.shape(inputs)[2]
        channels = inputs.shape[-1]
        
        # Reshape to (batch_size, height*width, channels)
        x = tf.reshape(inputs, (batch_size, height * width, channels))
        
        # Compute attention
        Q = self.W_q(x)  # (batch_size, height*width, units)
        K = self.W_k(x)  # (batch_size, height*width, units)
        V = self.W_v(x)  # (batch_size, height*width, units)
        
        # Attention scores
        attention_scores = tf.matmul(Q, K, transpose_b=True)
        attention_scores = attention_scores / tf.sqrt(tf.cast(self.units, tf.float32))
        attention_weights = self.softmax(attention_scores)
        
        # Apply attention
        attended = tf.matmul(attention_weights, V)
        
        # Reshape back
        attended = tf.reshape(attended, (batch_size, height, width, self.units))
        
        return attended
    
    def get_config(self):
        config = super(AttentionBlock, self).get_config()
        config.update({"units": self.units})
        return config

class ResNetBlock(layers.Layer):
    """ResNet building block for spectrograms"""
    
    def __init__(self, filters: int, kernel_size: int = 3, stride: int = 1, **kwargs):
        super(ResNetBlock, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.stride = stride
        
        self.conv1 = layers.Conv2D(filters, kernel_size, stride, padding='same')
        self.bn1 = layers.BatchNormalization()
        self.conv2 = layers.Conv2D(filters, kernel_size, 1, padding='same')
        self.bn2 = layers.BatchNormalization()
        
        # Shortcut connection
        if stride != 1:
            self.shortcut = layers.Conv2D(filters, 1, stride, padding='same')
            self.shortcut_bn = layers.BatchNormalization()
        else:
            self.shortcut = None
            
    def call(self, inputs, training=False):
        # Main path
        x = self.conv1(inputs)
        x = self.bn1(x, training=training)
        x = tf.nn.relu(x)
        
        x = self.conv2(x)
        x = self.bn2(x, training=training)
        
        # Shortcut path
        if self.shortcut:
            shortcut = self.shortcut(inputs)
            shortcut = self.shortcut_bn(shortcut, training=training)
        else:
            shortcut = inputs
            
        # Add shortcut
        x = x + shortcut
        x = tf.nn.relu(x)
        
        return x
    
    def get_config(self):
        config = super(ResNetBlock, self).get_config()
        config.update({
            "filters": self.filters,
            "kernel_size": self.kernel_size,
            "stride": self.stride
        })
        return config

def create_resnet_model(input_shape: Tuple[int, int, int] = None, 
                       num_classes: int = None) -> Model:
    """Create ResNet model for spectrogram classification"""
    input_shape = input_shape or config.model.input_shape
    num_classes = num_classes or config.model.num_classes
    
    inputs = layers.Input(shape=input_shape)
    
    # Initial convolution
    x = layers.Conv2D(64, 7, 2, padding='same')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.MaxPooling2D(3, 2, padding='same')(x)
    
    # ResNet blocks
    x = ResNetBlock(64)(x)
    x = ResNetBlock(64)(x)
    
    x = ResNetBlock(128, stride=2)(x)
    x = ResNetBlock(128)(x)
    
    x = ResNetBlock(256, stride=2)(x)
    x = ResNetBlock(256)(x)
    
    x = ResNetBlock(512, stride=2)(x)
    x = ResNetBlock(512)(x)
    
    # Global average pooling
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(config.model.dropout_rate)(x)
    
    # Classification head
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs, outputs, name='ResNet_Spectrogram')
    return model

def create_attention_model(input_shape: Tuple[int, int, int] = None,
                          num_classes: int = None) -> Model:
    """Create attention-based model for spectrogram classification"""
    input_shape = input_shape or config.model.input_shape
    num_classes = num_classes or config.model.num_classes
    
    inputs = layers.Input(shape=input_shape)
    
    # Feature extraction
    x = layers.Conv2D(64, 3, padding='same')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.MaxPooling2D(2)(x)
    
    x = layers.Conv2D(128, 3, padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.MaxPooling2D(2)(x)
    
    x = layers.Conv2D(256, 3, padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    
    # Attention mechanism
    x = AttentionBlock(256)(x)
    
    # More convolutions
    x = layers.Conv2D(512, 3, padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.MaxPooling2D(2)(x)
    
    # Global average pooling
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(config.model.dropout_rate)(x)
    
    # Classification
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs, outputs, name='Attention_Spectrogram')
    return model

def create_siamese_model(input_shape: Tuple[int, int, int] = None,
                        num_classes: int = None) -> Model:
    """Create Siamese-like network for spectrogram classification"""
    input_shape = input_shape or config.model.input_shape
    num_classes = num_classes or config.model.num_classes
    
    def create_feature_extractor():
        """Shared feature extractor"""
        model = keras.Sequential([
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2),
            
            layers.Conv2D(128, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2),
            
            layers.Conv2D(256, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2),
            
            layers.Conv2D(512, 3, padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.GlobalAveragePooling2D(),
            
            layers.Dense(256, activation='relu'),
            layers.Dropout(config.model.dropout_rate)
        ])
        return model
    
    # Shared feature extractor
    feature_extractor = create_feature_extractor()
    
    # Input
    inputs = layers.Input(shape=input_shape)
    
    # Extract features
    features = feature_extractor(inputs)
    
    # Classification head
    outputs = layers.Dense(num_classes, activation='softmax')(features)
    
    model = Model(inputs, outputs, name='Siamese_Spectrogram')
    return model

def create_simple_cnn(input_shape: Tuple[int, int, int] = None,
                     num_classes: int = None) -> Model:
    """Create a simple CNN baseline model"""
    input_shape = input_shape or config.model.input_shape
    num_classes = num_classes or config.model.num_classes
    
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        
        layers.Conv2D(32, 3, activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2),
        
        layers.Conv2D(64, 3, activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2),
        
        layers.Conv2D(128, 3, activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2),
        
        layers.Conv2D(256, 3, activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.GlobalAveragePooling2D(),
        
        layers.Dropout(config.model.dropout_rate),
        layers.Dense(128, activation='relu'),
        layers.Dropout(config.model.dropout_rate),
        layers.Dense(num_classes, activation='softmax')
    ], name='Simple_CNN')
    
    return model

def get_model(model_type: str = "resnet", **kwargs) -> Model:
    """Factory function to create models"""
    models = {
        "resnet": create_resnet_model,
        "attention": create_attention_model,
        "siamese": create_siamese_model,
        "simple_cnn": create_simple_cnn
    }
    
    if model_type not in models:
        raise ValueError(f"Unknown model type: {model_type}. Available: {list(models.keys())}")
    
    return models[model_type](**kwargs)
