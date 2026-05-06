import gradio as gr
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import os
from datetime import datetime
from ultralytics import YOLO

# ------------------------------------------
# 1. Device & Models
# ------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Style classifier (your existing code)
model = models.mobilenet_v2(weights=None)
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

# YOLOv8 nano object detector (auto‑downloads on first run)
detector = YOLO("yolov8n.pt")

# Furniture‑related COCO classes (we filter to only these)
FURNITURE_CLASSES = [
    'chair', 'couch', 'bed', 'dining table', 'tv', 'laptop',
    'refrigerator', 'sink', 'potted plant', 'vase', 'clock',
    'book', 'wine glass', 'cup', 'bowl', 'bottle', 'cell phone',
    'remote', 'teddy bear', 'scissors', 'hair drier'  # some home items
]

# ------------------------------------------
# 2. Style prediction (unchanged, returns confidence)
# ------------------------------------------
def predict_style(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406], [0.229,0.224,0.225])
    ])
    img_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(img_tensor)
        probs = torch.nn.functional.softmax(out, dim=1)
        conf, pred = torch.max(probs, 1)
    return class_names[pred.item()], conf.item()

# ------------------------------------------
# 3. Color extraction (unchanged)
# ------------------------------------------
def extract_palette(image, k=5):
    img = np.array(image.convert('RGB'))
    pixels = img.reshape(-1, 3).astype(np.float32)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels)
    centers = kmeans.cluster_centers_.astype(int)
    return [f"#{r:02x}{g:02x}{b:02x}" for r,g,b in centers]

# ------------------------------------------
# 4. Style‑based recommendations (base template)
# ------------------------------------------
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

# ------------------------------------------
# 5. Personalized advice generator (NEW)
# ------------------------------------------
def generate_personalized_advice(detected_objects, style):
    """Returns extra suggestions based on detected items."""
    advices = []
    obj_set = set(detected_objects)

    # Room function hints based on objects
    if 'couch' in obj_set or 'chair' in obj_set:
        advices.append("🛋️ We see seating – a textured throw and accent pillows will enhance the "
                       f"{style.lower()} look.")
    if 'bed' in obj_set:
        advices.append("🛏️ A bed is present – consider a stylish headboard and layered bedding for more comfort.")
    if 'dining table' in obj_set:
        advices.append("🍽️ A dining table is visible – a centerpiece or a statement light above it adds elegance.")
    if 'tv' in obj_set:
        advices.append("📺 TV detected – mount it at eye level and hide cables for a clean finish.")
    if 'potted plant' in obj_set or 'vase' in obj_set:
        advices.append("🌿 Plants bring life – you already have some, keep them well‑lit and trimmed.")
    if 'laptop' in obj_set:
        advices.append("💻 Workspace spotted – a proper desk and ergonomic chair could boost productivity.")
    if not advices:
        advices.append("We didn't detect specific furniture, but our style‑based recommendations still apply.")
    return advices

# ------------------------------------------
# 6. Main processing (FIXED indentation)
# ------------------------------------------
def process_image(image):
    if image is None:
        return (
            "<div style='padding:20px; background:white; color:black;'>⚠️ Please upload an image first, then click Analyze.</div>",
            gr.update(visible=False),
            gr.update(visible=False),
            ""
        )

    # Run style & palette
    style, confidence = predict_style(image)
    palette = extract_palette(image)

    # Run YOLO object detection
    results = detector(image, verbose=False)   # suppress logging
    detected_raw = []
    if results[0].boxes is not None:
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = detector.names[cls_id]
            detected_raw.append(label)

    # Filter only furniture‑related items, remove duplicates
    detected_furniture = list(set([item for item in detected_raw if item in FURNITURE_CLASSES]))
    # For display, sort alphabetically
    detected_furniture.sort()

    # Build swatches
    swatches_html = ""
    for hexc in palette:
        swatches_html += f"""
        <div style="display: inline-block; margin: 8px; text-align: center;">
            <div style="background-color: {hexc}; width: 80px; height: 80px; border-radius: 12px; border: 1px solid #aaa;"></div>
            <div style="font-family: monospace; margin-top: 5px; color: #1e1e2f; background: white; padding: 2px 4px; border-radius: 4px;">{hexc}</div>
        </div>
        """

    # Base recommendations
    rec = recommendations[style]

    # Personalized advice from YOLO findings
    personalized = generate_personalized_advice(detected_furniture, style)
    personalized_html = "".join([f"<li>{adv}</li>" for adv in personalized])

    # Detected items as badges
    if detected_furniture:
        badges = " ".join([f"<span class='badge'>{item}</span>" for item in detected_furniture])
    else:
        badges = "No specific furniture detected"

    # CORRECTED: html_output is OUTSIDE the if/else (properly indented)
    html_output = f"""
    <style>
        #ida-output, #ida-output * {{
            color: #000000 !important;
        }}
        #ida-output h2, #ida-output h3 {{
            color: #000000 !important;
        }}
        #ida-output .badge {{
            display: inline-block;
            background: #e0e7ff;
            padding: 4px 10px;
            border-radius: 12px;
            margin-right: 5px;
            color: #000000 !important;
        }}
    </style>
    <div id="ida-output" style="font-family: 'Segoe UI', Arial, sans-serif; background-color: white; padding: 20px; border-radius: 16px; margin: 10px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h2>🎨 Detected Style: <span>{style}</span></h2>
        <p style="font-size:1.1em;">Model confidence: <b>{confidence*100:.1f}%</b></p>
        <h3>🔍 Objects in Your Room</h3>
        <div style="margin-bottom:20px;">{badges}</div>
        <h3>🖌️ Color Palette</h3>
        <div style="margin-bottom: 20px;">{swatches_html}</div>
        <div style="background: #f0f0f0; padding: 15px; border-radius: 12px; margin-top: 15px;">
            <h3>🛋️ Furniture Suggestions ({style})</h3>
            <p>{rec['furniture']}</p>
            <h3>💡 Personalized Tips (based on detected objects)</h3>
            <ul style="text-align:left; margin-left: 20px;">{personalized_html}</ul>
            <h3>📐 Layout Advice</h3>
            <p>{rec['layout']}</p>
            <h3>💡 Lighting Tips</h3>
            <p>{rec['lighting']}</p>
        </div>
    </div>
    """

    # File name for feedback
    try:
        fname = os.path.basename(image.filename) if hasattr(image, 'filename') and image.filename else "uploaded_image"
    except Exception:
        fname = "uploaded_image"

    return html_output, gr.update(visible=True), gr.update(visible=True), fname

# ------------------------------------------
# 7. Feedback (unchanged)
# ------------------------------------------
def log_feedback(vote, image_name):
    if vote is None or image_name == "":
        return ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_file = "feedback.csv"
    file_exists = os.path.isfile(feedback_file)
    with open(feedback_file, "a", newline="") as f:
        if not file_exists:
            f.write("timestamp,image_name,vote\n")
        f.write(f"{timestamp},{image_name},{vote}\n")
    return f"✅ Thank you! Your {vote} feedback has been recorded."

# ------------------------------------------
# 8. Example loader (unchanged)
# ------------------------------------------
def load_example():
    example_path = "example.jpg"
    if os.path.exists(example_path):
        return Image.open(example_path)
    else:
        return None

# ------------------------------------------
# 9. Gradio UI (unchanged)
# ------------------------------------------
with gr.Blocks(title="Interior Design Advisor", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏡 Interior Design Advisor")
    gr.Markdown("Upload a photo of a room, then click **Analyze Room**. Or try our example image.")

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload a Room Photo", sources=["upload"])
            with gr.Row():
                analyze_btn = gr.Button("🔍 Analyze Room", variant="primary")
                example_btn = gr.Button("📸 Try an Example")
        with gr.Column():
            output_html = gr.HTML(label="Design Recommendations",
                                  value="<div style='padding:20px; text-align:center; background:#f0f0f0; border-radius:16px;'>Awaiting analysis...</div>")
            with gr.Group(visible=False) as feedback_group:
                gr.Markdown("### Was this helpful?")
                with gr.Row():
                    thumb_up = gr.Button("👍 Thumbs Up")
                    thumb_down = gr.Button("👎 Thumbs Down")
                feedback_status = gr.Textbox(label="", interactive=False)

    current_image_name = gr.State("")

    analyze_btn.click(
        fn=process_image,
        inputs=image_input,
        outputs=[output_html, feedback_group, feedback_group, current_image_name]
    )

    example_btn.click(
        fn=load_example,
        inputs=None,
        outputs=image_input
    )

    thumb_up.click(
        fn=lambda img_name: log_feedback("positive", img_name),
        inputs=current_image_name,
        outputs=feedback_status
    )
    thumb_down.click(
        fn=lambda img_name: log_feedback("negative", img_name),
        inputs=current_image_name,
        outputs=feedback_status
    )

demo.launch(ssr_mode=False)