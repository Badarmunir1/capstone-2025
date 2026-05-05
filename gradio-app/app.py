import gradio as gr
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# Disable SSR (fix for asyncio error) and set share=False
# Also remove theme from constructor to avoid deprecation warning

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model
model = models.mobilenet_v2(weights=None)  # Use weights=None instead of pretrained=False
model.classifier = torch.nn.Sequential(
    torch.nn.Dropout(0.2),
    torch.nn.Linear(model.last_channel, 128),
    torch.nn.ReLU(),
    torch.nn.Linear(128, 4)
)
model.load_state_dict(torch.load('best_style_model.pth', map_location=device))
model.eval()
model.to(device)

class_names = ['Classic', 'Minimalist', 'Modern', 'Rustic']

def predict_style(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406], [0.229,0.224,0.225])
    ])
    img_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(img_tensor)
        pred = torch.argmax(out, 1).item()
    return class_names[pred]

def extract_palette(image, k=5):
    img = np.array(image.convert('RGB'))
    pixels = img.reshape(-1, 3).astype(np.float32)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels)
    centers = kmeans.cluster_centers_.astype(int)
    return [f"#{r:02x}{g:02x}{b:02x}" for r,g,b in centers]

recommendations = {
    "Modern": {
        "furniture": "Clean lines, metal/glass surfaces, neutral upholstery",
        "layout": "Open plan, minimal clutter, statement artwork",
        "lighting": "Track lighting, large windows, LED strips"
    },
    "Minimalist": {
        "furniture": "Functional pieces, hidden storage, monochrome tones",
        "layout": "Plenty of negative space, simple shapes",
        "lighting": "Recessed lights, natural light priority"
    },
    "Rustic": {
        "furniture": "Reclaimed wood, leather sofa, wrought iron details",
        "layout": "Cozy, central fireplace or focal point",
        "lighting": "Warm bulbs, lanterns, wrought iron chandeliers"
    },
    "Classic": {
        "furniture": "Tufted sofas, dark wood, elegant details",
        "layout": "Symmetrical, formal seating areas",
        "lighting": "Crystal chandeliers, sconces"
    }
}

def interior_advisor(image):
    if image is None:
        return "<div style='padding:20px; background:white; color:black;'>⚠️ Please upload an image.</div>"
    style = predict_style(image)
    palette = extract_palette(image)
    rec = recommendations[style]
    swatches_html = ""
    for hexc in palette:
        swatches_html += f"""
        <div style="display: inline-block; margin: 8px; text-align: center;">
            <div style="background-color: {hexc}; width: 80px; height: 80px; border-radius: 12px; border: 1px solid #aaa;"></div>
            <div style="font-family: monospace; margin-top: 5px; color: #1e1e2f; background: white; padding: 2px 4px; border-radius: 4px;">{hexc}</div>
        </div>
        """
    html_output = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; color: #1e1e2f; background-color: white; padding: 20px; border-radius: 16px; margin: 10px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h2 style="color: #1e1e2f;">🎨 Detected Style: <span style="color: #2c3e50;">{style}</span></h2>
        <h3 style="color: #1e1e2f;">🖌️ Color Palette</h3>
        <div style="margin-bottom: 20px;">{swatches_html}</div>
        <div style="background: #f5f5f5; padding: 15px; border-radius: 12px; margin-top: 15px;">
            <h3 style="color: #1e1e2f;">🛋️ Furniture Suggestions</h3>
            <p style="color: #1e1e2f;">{rec['furniture']}</p>
            <h3 style="color: #1e1e2f;">📐 Layout Advice</h3>
            <p style="color: #1e1e2f;">{rec['layout']}</p>
            <h3 style="color: #1e1e2f;">💡 Lighting Tips</h3>
            <p style="color: #1e1e2f;">{rec['lighting']}</p>
        </div>
    </div>
    """
    return html_output

# Gradio 6.0: theme moved to launch(), and we disable SSR to avoid asyncio error
iface = gr.Interface(
    fn=interior_advisor,
    inputs=gr.Image(type="pil", label="Upload a Room Photo"),
    outputs=gr.HTML(label="Design Recommendations"),
    title="Interior Design Advisor",
    description="Upload a photo of a room – AI predicts style, extracts colors, gives design advice."
)

iface.launch(ssr_mode=False)   # disables server-side rendering to avoid file descriptor error