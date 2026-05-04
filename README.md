# 🏠 Interior Design Advisor (IDA)

**AI-Powered Room Design Assistant**  
*Computer Vision Capstone Project 2025*

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)

🌐 **Live Demo:** [Hugging Face Space](https://huggingface.co/spaces/AbnormalCreation/interior-design-advisor)

---

## 📋 Overview

Interior Design Advisor (IDA) takes a photo of any room and instantly provides **personalized design insights**: a detected interior style (Modern, Minimalist, Rustic, Classic), a 5‑color palette extracted from the image, and tailored furniture, layout & lighting recommendations.

This repository documents the full project journey, from early prototyping and experimentation to the final deployed application.

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
| `gradio-app/` | **Final submission** – the PyTorch + Gradio app deployed on Hugging Face |
| `app/` and `notebooks/` | Early prototype – TensorFlow/Keras + Streamlit experiments |
| `docs/` | Architecture diagrams, SRS, design documents, weekly reports |
| `diagrams/` | Editable architecture diagrams (component, deployment, ERD, etc.) |
| `data/` | Sample images and instructions for obtaining the full dataset |
| `src/` | Experimental helper functions (used during prototyping) |

The **final, live version** lives in `gradio-app/`. The older code is preserved as a record of the experimentation phase.

---

## 🔄 Project Evolution & Experiments

### 1. Initial Prototype (TensorFlow / Streamlit)
- **Framework:** TensorFlow / Keras, Streamlit
- **Model:** MobileNetV2 (pretrained on ImageNet), fine‑tuned on a custom dataset
- **Classes:** Originally 5 styles (Modern, Minimalist, Industrial, Bohemian, Rustic)
- **Deployment:** Local Streamlit app (`app/ida_app.py`)
- **Why we moved away:**
  - PyTorch offered easier export and Hugging Face integration
  - The 5‑class model struggled with Industrial and Bohemian due to limited data
  - Streamlit required more server resources than Gradio on free hosting

### 2. Final Version (PyTorch / Gradio)
- **Framework:** PyTorch, torchvision, Gradio
- **Model:** MobileNetV2 with a custom classifier head → 4 classes
- **Classes:** Modern, Minimalist, Rustic, Classic *(Industrial and Bohemian dropped due to low per‑class accuracy and data scarcity)*
- **Training:** Performed in Google Colab with a T4 GPU; final validation accuracy ~72%
- **Color Extraction:** K‑Means clustering (k=5) on pixel colors → HEX codes
- **Deployment:** Hosted on Hugging Face Spaces with a Gradio interface (`gradio-app/app.py`)

---

## 🧪 Dataset & Training Details

- **Source:** Publicly available interior design images (Kaggle, Unsplash), manually cleaned and labelled
- **Size:** ~3,000 images (after cleaning), split 80/10/10
- **Augmentations:** Random horizontal flip, rotation (±15°), color jitter, random resized crop
- **Preprocessing:** Resize to 224×224, normalize with ImageNet mean/std
- **Training:** CrossEntropyLoss, Adam optimizer (lr=1e-4), batch size 32, early stopping
- **Validation accuracy:** 72% (4‑class balanced accuracy ~70%)

**Why 72%?**  
Interior style is subjective; rooms often mix styles. Limited dataset size and label noise prevented higher accuracy, but the model reliably distinguishes the four core styles for clearly‑styled rooms.

---

## ⚙️ How to Run Locally (Final App)

1. Clone the repo:
   ```bash
   git clone https://github.com/Badarmunir1/capstone-2025.git
   cd capstone-2025/gradio-app

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   python app.py
   
4. Open the local URL (usually http://127.0.0.1:7860) in your browser.

Key Strengths
End‑to‑end working demo that runs reliably on free cloud resources

Modular code structure – Gradio app separate from training pipeline

Transparent limitations are openly discussed (see below)

Comprehensive documentation – SRS, SDS, architecture diagrams, weekly reports

Easy setup via a single requirements.txt

🚧 Limitations & Known Issues
🔹 Static Recommendations
The furniture/layout/lighting advice is currently template‑based and not yet personalised to the uploaded image’s contents. This is a planned improvement beyond the capstone timeline.

🔹 Limited Style Coverage
Only four styles are supported. Adding more styles requires a broader and more balanced dataset.

🔹 Model Accuracy
Accuracy ~72% means the model will misclassify borderline or mixed‑style rooms. We mitigate this by displaying the detected style and acknowledging that ambiguous rooms may get a wrong – but still plausible – result.

🔹 Pickle Security Warning in Hugging Face
The file best_style_model.pth is a standard PyTorch serialized model. Hugging Face’s security scanner flags it because of pickle imports (which PyTorch uses internally). This file is entirely safe – it contains only our own trained weights. No arbitrary code execution will occur. The warning can be safely ignored.

🔹 Resource Constraints
Training: Limited to Google Colab’s free GPU hours; hyperparameter tuning was minimal.

Data: A larger, professionally labelled dataset would significantly boost accuracy.

Hosting: Free Hugging Face Spaces may sleep after inactivity; first load may take ~30 seconds.

🔮 Future Work
Replace static recommendations with a LLM‑based generator that uses extracted room features (dominant colour, detected objects) to produce truly personalised advice.

Expand the style classifier to 8–10 styles, possibly using a hierarchical approach.

Add object detection (YOLO / Faster R‑CNN) to identify furniture pieces and suggest swaps.

Integrate a feedback loop (thumbs up/down) to continuously improve the model.

Optimise model for edge deployment (ONNX / TensorRT) to run on low‑power devices.

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

- **Live App:** [Hugging Face Space](https://huggingface.co/spaces/AbnormalCreation/interior-design-advisor)
- **GitHub Repo:** [capstone-2025](https://github.com/Badarmunir1/capstone-2025)

🏆 Acknowledgements
Pre‑trained MobileNetV2 from PyTorch Image Models (TIMM) and TensorFlow/Keras

Hugging Face for free hosting

Open source libraries: Gradio, OpenCV, scikit‑learn, Pillow


Capstone project submitted to the Department of Computer Science, University of Sargodha, in partial fulfilment of the requirements for the degree of Bachelor of Science in Computer Science (BSCS), Batch 2022–2026.
