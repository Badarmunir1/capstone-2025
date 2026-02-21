# src/core.py - AI Helper Functions for IDA App & Notebooks (Fixed OpenCV Depth Error)

import cv2
import numpy as np
from sklearn.cluster import KMeans
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

def preprocess_image(image_bytes, target_size=(224, 224)):
    """Full preprocessing pipeline with type fixes for OpenCV error"""
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Cannot load image")
    
    # Ensure 3 channels and uint8
    if len(img.shape) == 2:  # Grayscale
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = img.astype(np.uint8)
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = img_rgb.astype(np.uint8)  # Ensure uint8 after conversion
    
    # Resize
    img_resized = cv2.resize(img_rgb, target_size)
    img_resized = img_resized.astype(np.uint8)
    
    # Denoise
    img_denoised = cv2.fastNlMeansDenoisingColored(cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR), None, 10, 10, 7, 21)
    img_denoised = cv2.cvtColor(img_denoised, cv2.COLOR_BGR2RGB)
    img_denoised = img_denoised.astype(np.uint8)
    
    # CLAHE
    lab = cv2.cvtColor(img_denoised, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))
    enhanced_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
    enhanced_rgb = enhanced_rgb.astype(np.uint8)  # Ensure uint8 after final conversion
    
    return enhanced_rgb, img_rgb

def extract_color_palette(image_rgb, n_colors=5):
    """K-Means in LAB space"""
    lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
    pixels = lab.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)
    
    colors_lab = kmeans.cluster_centers_.astype(int)
    colors_rgb = cv2.cvtColor(colors_lab.reshape(1, n_colors, 3), cv2.COLOR_LAB2RGB).reshape(-1, 3)
    
    labels = kmeans.labels_
    counts = np.bincount(labels)
    percentages = (counts / len(labels)) * 100
    
    hex_colors = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in colors_rgb]
    
    return colors_rgb, hex_colors, percentages

def detect_style(image_rgb, features, custom_model):
    """Improved detection with custom model if available"""
    if custom_model:
        # Predict with custom model
        img_array = np.expand_dims(cv2.resize(image_rgb, (224, 224)), axis=0)
        img_pre = preprocess_input(img_array)
        preds = custom_model.predict(img_pre)[0]
        pred_class = np.argmax(preds)  # Get top class index
        # Map to your 5 styles (assume class_indices from training)
        # Example: class_indices = train_generator.class_indices
        # For simplicity, assume mapping
        mapped_style = style_map.get(list(style_map.keys())[pred_class % len(style_map)], 'Modern')
    else:
        # Fallback rule-based
        brightness = np.mean(image_rgb)
        color_variance = np.var(image_rgb)
        edge_density = np.sum(cv2.Canny(cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY), 100, 200) > 0) / (image_rgb.shape[0] * image_rgb.shape[1])
        feat_mean = np.mean(features)
        
        if brightness > 180 and edge_density < 0.08 and color_variance < 1500:
            mapped_style = "Minimalist"
        elif edge_density > 0.25 or feat_mean > 2.5:
            mapped_style = "Industrial"
        elif len(np.unique(np.round(image_rgb / 30), axis=0)) > 8:
            mapped_style = "Bohemian"
        elif brightness < 110:
            mapped_style = "Rustic"
        else:
            mapped_style = "Modern"
    
    return mapped_style

def get_recommendations(style, colors_rgb, hex_colors):
    recs = {
        'Minimalist': "Clean lines, white/gray walls, simple furniture, lots of negative space.",
        'Modern': "Sleek sofas, geometric patterns, metal accents, bold lighting.",
        'Industrial': "Exposed brick, metal shelves, leather, raw wood, dark tones.",
        'Bohemian': "Layered textiles, plants, vintage rugs, colorful pillows, macramé.",
        'Rustic': "Warm wood, stone, cozy blankets, earthy tones, natural textures."
    }
    
    color_tip = f"Recommended wall color: {hex_colors[0]} | Accent: {hex_colors[1]}"
    return f"{recs.get(style, recs['Modern'])} {color_tip}"

style_map = {
    'living_room': 'Modern',
    'bed_room': 'Minimalist',
    'airport': 'Industrial',
    'artstudio': 'Bohemian',
    'closet': 'Rustic',
    # Add more...
}