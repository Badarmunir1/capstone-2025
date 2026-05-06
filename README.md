# 🏠 Interior Design Advisor (IDA)

**AI-Powered Room Design Assistant**  
*Computer Vision Capstone Project 2025*

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-00FFFF?style=for-the-badge&logo=yolo&logoColor=black)

🌐 **Live Demos:**  
- **Latest (v2):** [Interior Design Advisor v2](https://huggingface.co/spaces/AbnormalCreation/Interior_design_advisor_v2) *(with object detection & personalised tips)*  
- **Original (v1):** [Interior Design Advisor](https://huggingface.co/spaces/AbnormalCreation/interior-design-advisor)

---

## 📋 Overview

Interior Design Advisor (IDA) takes a photo of any room and instantly provides **personalised design insights**:

- 🎨 **5‑colour palette** (extracted with K‑Means)  
- 🧠 **Style classification** (Modern, Minimalist, Rustic, Classic) with **confidence score**  
- 🔍 **Object detection** (YOLOv8) – identifies furniture & items already in the room  
- 💡 **Personalised advice** – tailored tips based on what was detected  
- 👍 **User feedback** – thumbs‑up / thumbs‑down to improve the tool  

All wrapped in an easy‑to‑use Gradio interface, **running live on Hugging Face Spaces** (free CPU).

---

## 👥 Team & Institution

| Role | Name |
|------|------|
| **Project Manager** | Dr. Muhammad Illyas |
| **Project Supervisor** | Dr. Faisal Shehzad |
| **Team Members** | Badar Munir, Sana Jabbar, Hafsa Hadi |
| **Batch** | 2022–2026 |
| **Department** | Computer Science (BSCS) |
| **University** | University of Sargodha |

---

## 📁 Repository Overview

| Folder / File | Purpose |
|---------------|---------|
| `gradio-appv2/` | **Final enhanced app (v2)** – Gradio + YOLOv8 object detection, personalised tips, confidence, feedback, example image |
| `gradio-app/` | First deployed app (v1) – Gradio with style classification & colour extraction |
| `app/` and `notebooks/` | Early prototypes – TensorFlow/Keras + Streamlit experiments |
| `docs/` | Architecture diagrams, SRS, design documents, weekly reports |
| `diagrams/` | Editable architecture diagrams (component, deployment, ERD, etc.) |
| `data/` | Sample images and dataset instructions |
| `src/` | Experimental helper functions (used during prototyping) |

The **latest, most advanced version** is inside `gradio-appv2/`. Older versions are kept for reference.

---

## 🔄 Project Evolution

### 1. Initial Prototype (TensorFlow / Streamlit)
- **Framework:** TensorFlow / Keras, Streamlit  
- **Model:** MobileNetV2 (pretrained on ImageNet), 5 styles  
- **Why we moved:** Limited accuracy on rare styles, harder deployment, PyTorch better for Hugging Face

### 2. First Gradio Deployment (v1)
- **Framework:** PyTorch, Gradio  
- **Model:** MobileNetV2 (4 classes)  
- **Features:** Colour palette, style classification, static recommendations  
- **Limitations:** Advice was template‑based, no understanding of actual room contents  

### 3. Enhanced Version (v2) – Current Final Submission
- **Framework:** PyTorch, Gradio, **Ultralytics YOLOv8**  
- **New Features:**
  - Object detection (sofa, chair, bed, table, plant, TV, etc.)  
  - Confidence score for style prediction  
  - Personalised advice based on detected objects  
  - “Try an Example” button for instant demo  
  - User feedback collection (thumbs up/down)  
- **Deployment:** [Hugging Face Space v2](https://huggingface.co/spaces/AbnormalCreation/Interior_design_advisor_v2)  
- **Result:** The app now **truly analyses the room** rather than returning generic suggestions.

---

## 🧪 Dataset & Training Details

- **Source:** Publicly available interior design images (Kaggle, Unsplash), manually cleaned & labelled  
- **Size:** ~3,000 images (80/10/10 split)  
- **Augmentations:** Flip, rotation, colour jitter, random crop  
- **Preprocessing:** Resize 224×224, ImageNet normalisation  
- **Training:** CrossEntropyLoss, Adam (lr=1e-4), batch size 32, early stopping  
- **Validation accuracy:** ~72% (4‑class)  

**Why 72%?**  
Interior style is subjective; rooms often mix styles. Dataset size and label noise limited further gains, but the model reliably separates the four core styles.

---

## ⚙️ How to Run Locally (v2 Enhanced App)

1. Clone the repo:
   ```bash
   git clone https://github.com/Badarmunir1/capstone-2025.git
   cd capstone-2025/gradio-appv2
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open `http://127.0.0.1:7860` in your browser.

---

## 🧠 Key Strengths

- **Working live demo** on free cloud infrastructure (Hugging Face Spaces)  
- **Object detection** turns a blind classifier into a room‑aware advisor  
- **Confidence scores** add transparency and trust  
- **Personalised tips** evolve beyond static templates  
- **User feedback** loop built‑in for continual improvement  
- **Comprehensive documentation** (SRS, SDS, architecture diagrams, reports)  
- **Modular code** – separate apps for v1 and v2, easy to compare

---

## 🚧 Limitations & Known Issues

### 🔹 Advice Still Partially Template‑Based
Personalised tips are rule‑based; they react to detected objects but don’t generate fully novel advice. An LLM‑based approach is planned for the future.

### 🔹 Limited Style Coverage
Only four styles are currently supported. Expanding requires a larger, well‑balanced dataset.

### 🔹 Model Accuracy
~72% accuracy means borderline/mixed rooms can be misclassified. Confidence scores help indicate uncertainty.

### 🔹 Pickle Security Warning (Hugging Face)
`best_style_model.pth` is a standard PyTorch file. The platform’s pickle warning is safe to ignore – it contains only our trained weights.

### 🔹 Resource Constraints
- Training: limited to free Colab GPU hours  
- Data: more professional labels would boost accuracy  
- Hosting: free Spaces may sleep after inactivity (first load ~30 s)

---

## 🔮 Future Work

- Integrate an **LLM** to generate rich, fully personalised room descriptions  
- Expand to 8–10 design styles  
- Add **real‑time webcam** capture  
- Connect to **furniture e‑commerce APIs** for direct product linking  
- Optimise model for **edge deployment** (ONNX / TensorRT)

---

## 📄 Documentation

- [SRS Document](docs/IDA_SRS.pdf)  
- [Design Document](docs/IDA_Design_Document.pdf)  
- [Proposal](docs/IDA_Proposal.pdf)  
- [Architecture Diagram](docs/IDA_Architecture_Diagram.pdf)  
- [Signed SRS](docs/IDA_SRS_Signed.pdf)  
- [Presentation](docs/IDA_Presentation.pdf)  
- [10 Week Report](docs/10_week_report.pdf)  
- [Weekly Report 24 Nov](docs/Weekly_Report_24_Nov.pdf)

## 🖼 Diagrams (Editable)

View and edit in [draw.io](https://app.diagrams.net/):

- [Component Diagram](diagrams/component.drawio)  
- [Deployment Diagram](diagrams/deployment.drawio)  
- [ERD](diagrams/erd.drawio)  
- [Package Diagram](diagrams/package.drawio)  
- [Physical Data Model](diagrams/physical%20data%20model.drawio)  
- [State Transition](diagrams/state%20transition.drawio)  
- [Subsystem Diagram](diagrams/Subsystem.drawio)

## 📎 Links

- **Live App (v2):** [Interior Design Advisor v2](https://huggingface.co/spaces/AbnormalCreation/Interior_design_advisor_v2)  
- **Original (v1):** [Interior Design Advisor](https://huggingface.co/spaces/AbnormalCreation/interior-design-advisor)  
- **GitHub Repo:** [capstone-2025](https://github.com/Badarmunir1/capstone-2025)

---

## 🏆 Acknowledgements

- Pre‑trained MobileNetV2 from PyTorch Image Models (TIMM) and TensorFlow/Keras  
- YOLOv8 by Ultralytics  
- Hugging Face for free hosting  
- Open source libraries: Gradio, OpenCV, scikit‑learn, Pillow  

---

*Capstone project submitted to the Department of Computer Science, University of Sargodha, in partial fulfilment of the requirements for the degree of Bachelor of Science in Computer Science (BSCS), Batch 2022–2026.*
