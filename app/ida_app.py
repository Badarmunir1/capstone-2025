# app/ida_app.py - Full AI Interior Design Advisor Streamlit App
# Run with: streamlit run app/ida_app.py (after setup)

import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Model, load_model
import matplotlib.pyplot as plt
from PIL import Image
import json
import os
from datetime import datetime
import io

# Load MobileNetV2 for Feature Extraction + Custom Trained Model
@st.cache_resource
def load_models():
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    feature_extractor = Model(inputs=base_model.input, outputs=base_model.output)
    
    # Load your trained model (from Day 1 integration)
    # Assume saved as models/mobilenetv2_indoor.h5 - adjust path if needed
    try:
        custom_model = load_model('../models/mobilenetv2_indoor.h5')
    except:
        st.warning("Custom model not found - using base MobileNetV2")
        custom_model = None
    
    return feature_extractor, custom_model

feature_extractor, custom_model = load_models()

# Style Mapping (from 67 Indoor classes to your 5 styles - expand as needed)
style_map = {
    'living_room': 'Modern',
    'bed_room': 'Minimalist',
    'airport': 'Industrial',
    'artstudio': 'Bohemian',
    'closet': 'Rustic',
    # Add more mappings for all 67 classes...
    # Default fallback in function
}

# Helper Functions (from core.py)
def preprocess_image(image_bytes, target_size=(224, 224)):
    """Full preprocessing pipeline"""
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Cannot load image")
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize
    img_resized = cv2.resize(img_rgb, target_size)
    
    # Denoise
    img_denoised = cv2.fastNlMeansDenoisingColored(cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR), None, 10, 10, 7, 21)
    img_denoised = cv2.cvtColor(img_denoised, cv2.COLOR_BGR2RGB)
    
    # CLAHE
    lab = cv2.cvtColor(img_denoised, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))
    enhanced_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
    
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

# Streamlit App UI
st.title("🛋️ AI-Powered Interior Design Advisor (IDA)")
st.markdown("Upload a room photo for instant color palette, style detection, and redesign suggestions!")

uploaded_file = st.file_uploader("Choose a room image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    try:
        image_bytes = uploaded_file.read()
        original_img = Image.open(io.BytesIO(image_bytes))
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(original_img, caption="Your Uploaded Room", use_column_width=True)
        
        # Analyze
        enhanced_rgb, original_rgb = preprocess_image(image_bytes)
        
        n_colors = st.slider("Number of Dominant Colors", 3, 8, 5)
        colors_rgb, hex_colors, percentages = extract_color_palette(enhanced_rgb, n_colors)
        
        img_array = np.expand_dims(cv2.resize(enhanced_rgb, (224, 224)), axis=0)
        img_pre = preprocess_input(img_array)
        features = feature_extractor.predict(img_pre, verbose=0)[0]
        flat_features = features.flatten()
        
        style = detect_style(enhanced_rgb, flat_features, custom_model)
        
        suggestions = get_recommendations(style, colors_rgb, hex_colors)
        
        # Palette Viz
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.imshow([colors_rgb / 255])
        ax.axis('off')
        for i, (hex_c, perc) in enumerate(zip(hex_colors, percentages)):
            ax.text(i, 0.5, f"{hex_c}\n{perc:.1f}%", ha='center', va='center', 
                    color='white' if np.mean(colors_rgb[i]) < 120 else 'black', fontsize=10)
        with col2:
            st.pyplot(fig, use_container_width=True)
        
        st.subheader("🎨 Detected Style")
        st.write(style)
        
        st.subheader("💡 Recommendations")
        st.write(suggestions)
        
        # After Redesign (static for now)
        st.subheader("✨ AI-Generated Redesign")
        after_path = f"data/suggested/{style.lower()}_after.jpg"
        if os.path.exists(after_path):
            st.image(after_path, caption=f"{style} Style After", use_column_width=True)
        else:
            st.warning("After image not found - add to data/suggested/")
        
        # Save Results
        result = {
            "timestamp": datetime.now().isoformat(),
            "style": style,
            "colors_hex": hex_colors,
            "percentages": percentages.tolist(),
            "recommendations": suggestions
        }
        st.download_button("Download Analysis JSON", json.dumps(result, indent=2), "ida_analysis.json")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")