---
title: Interior Design Advisor
emoji: 🏡
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 6.13.0
python_version: '3.10'
app_file: app.py
pinned: true
short_description: AI Powered Interior Designer
thumbnail: >-
  https://cdn-uploads.huggingface.co/production/uploads/68d771b4d8b96845c2d57bdf/DkkJyIrboIqFkdYJwEyYq.png
---




# 🏡 Interior Design Advisor

**AI‑Powered Room Design Assistant – Understand your room in seconds.**

[![Live Demo](https://img.shields.io/badge/Hugging%20Face-Space-blue)](https://huggingface.co/spaces/AbnormalCreation/Interior_design_advisor_v2)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-black)](https://github.com/Badarmunir1/capstone-2025)

Upload a photo of any room, click **Analyze Room**, and get a complete design report instantly:

- 🎨 **Dominant 5‑color palette** – extracted with K‑Means
- 🧠 **Style classification** – Modern, Minimalist, Rustic, or Classic (with confidence score)
- 🔍 **Object detection** – identifies furniture & items already in the room (YOLOv8)
- 💡 **Personalised advice** – tailored tips based on what was detected
- 👍 **User feedback** – thumbs‑up / thumbs‑down to improve the tool

No design experience needed – perfect for quick inspiration or planning your next makeover.

---

## 🚀 Live Demo

👉 **[Click here to try it now](https://huggingface.co/spaces/AbnormalCreation/Interior_design_advisor_v2)**

---

## 📸 Example Output

After uploading a living room photo, you’ll see something like:

> 🎨 Detected Style: **Modern** (confidence: 73.7%)  
> 🔍 Objects in Your Room: `couch` `tv`  
> 🖌️ Color Palette: `#374456` `#9ba7b5` `#5e7187` `#c8d3e0` `#1e2530`  
> 🛋️ Furniture Suggestions: Clean lines, metal/glass surfaces, neutral upholstery  
> 💡 Personalized Tips:  
>   - 🛋️ We see seating – a textured throw and accent pillows will enhance the modern look.  
>   - 📺 TV detected – mount it at eye level and hide cables for a clean finish.  
> 📐 Layout Advice: Open plan, minimal clutter, statement artwork  
> 💡 Lighting Tips: Track lighting, large windows, LED strips  

---

## 🛠️ Technologies Used

| Area | Tools |
|------|-------|
| **Deep Learning** | PyTorch, torchvision (MobileNetV2 fine‑tuned) |
| **Object Detection** | Ultralytics YOLOv8 (nano) |
| **Color Extraction** | OpenCV, scikit‑learn (K‑Means) |
| **Interface** | Gradio 5/6 (Blocks API) |
| **Hosting** | Hugging Face Spaces (free CPU) |

---

## 🧪 Run Locally

```bash
git clone https://huggingface.co/spaces/AbnormalCreation/Interior_design_advisor_v2
cd interior-design-advisor
pip install -r requirements.txt
python app.py
```
Then open `http://localhost:7860`.

---

## 🧠 Model Details

- **Style classifier**: MobileNetV2 with custom head (Dropout → 128 → ReLU → 4). Trained on ~3000 interior images, validation accuracy ~72%.
- **Object detector**: YOLOv8n (nano), pretrained on COCO; filtered to home‑related classes (sofa, chair, bed, table, plant, etc.).
- YOLO weights are auto‑downloaded on first run; the style model (`best_style_model.pth`) is included in the Space.

---

## 👥 Team (Capstone Project)

| Role | Name |
|------|------|
| **Group Leader** | Badar Munir |
| **Member** | Sana Jabbar |
| **Member** | Hafsa Hadi |
| **Project Advisor** | Dr. Faisal Shehzad |
| **Project Manager** | Dr. Muhammad Illyas |

*Department of Computer Science, University of Sargodha – Batch 2022‑2026*

---

## 📂 Repository Structure (Space)

```
interior-design-advisor/
├── app.py                 # Main Gradio application
├── best_style_model.pth   # Trained MobileNetV2 weights
├── requirements.txt       # Python dependencies
├── example.jpg            # Sample image for "Try an Example"
├── feedback.csv           # Collected feedback (generated automatically)
└── README.md              # This file
```

Full project documentation, diagrams, and earlier prototypes are on the [GitHub repository](https://github.com/Badarmunir1/capstone-2025).

---

## 📄 License

Academic project – please credit the authors if you reuse any part.

---

## 🙏 Acknowledgements

- MIT Indoor67 & Places365 datasets
- Gradio & Hugging Face for free tools
- Ultralytics for YOLOv8
- Our advisors for guidance

---

## ✨ Future Improvements

- Add more design styles (Industrial, Scandinavian, Bohemian)
- Real‑time webcam capture
- Furniture e‑commerce API integration
- LLM‑powered full room description

---

*Enjoy exploring your room’s potential!*