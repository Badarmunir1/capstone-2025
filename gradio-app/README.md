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




[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/AbnormalCreation/interior-design-advisor)
[![Gradio](https://img.shields.io/badge/Gradio-6.13.0-orange)](https://gradio.app)

## Source Code
Full project repository and documentation: [capstone-2025](https://github.com/Badarmunir1/capstone-2025)

**Interior Design Advisor** is an AI‑powered web application that helps you get professional interior design recommendations from a single room photo.  

Just upload an image, click **Analyze Room**, and the system will:
- 🎨 **Extract the dominant color palette** (5 colors with HEX codes)
- 🧠 **Classify the room style** – Modern, Minimalist, Rustic, or Classic
- 🛋️ **Generate personalized advice** for furniture, layout, and lighting

No design expertise required – instant inspiration for your next makeover.

---

## 🚀 Live Demo

Try it now on Hugging Face Spaces:  
👉 **[Interior Design Advisor](https://huggingface.co/spaces/AbnormalCreation/interior-design-advisor)**

---

## 📸 How It Works

1. **Upload** a photo of any room (bedroom, living room, kitchen, etc.)
2. **Click** the *Analyze Room* button
3. **Get** a complete design report:
   - Detected style
   - Color swatches with HEX codes
   - Furniture suggestions
   - Layout advice
   - Lighting tips

---

## 🛠️ Technologies Used

- **PyTorch** & **torchvision** – deep learning model (fine‑tuned MobileNetV2)
- **OpenCV** & **scikit‑learn** – K‑means color extraction
- **Gradio** – interactive web interface
- **Hugging Face Spaces** – free hosting (Python 3.10 + Gradio 6)

---

## 📂 Repository Structure

```
interior-design-advisor/
├── app.py                 # Main Gradio application
├── requirements.txt       # Python dependencies
├── best_style_model.pth   # Trained model weights (4 styles)
├── README.md              # This file
└── demo.png               # (optional) screenshot
```

---

## 🧪 Run Locally

### Prerequisites
- Python 3.9 – 3.11 (recommended)
- pip

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open `http://localhost:7860` in your browser.

---

## 📖 Model Training (Brief)

- **Base model**: MobileNetV2 (pretrained on ImageNet)
- **Dataset**: MIT Indoor67 mapped to 4 style classes
- **Training**: 15 epochs, ~5000 images, validation accuracy ~72%
- **Output**: `best_style_model.pth` (included)

For detailed training steps, see the Colab notebook (link if available).

---

## 👥 Team (Capstone Project)

- **Badar Munir** (Group Leader)  
- **Sana Jabbar**  
- **Hafsa Hadi**  

**Project Advisor**: Dr. Faisal Shahzad  
**Project Manager**: Dr. Muhammad Illyas  

---

## 📄 License

This project is for academic purposes only. Please credit the authors if you reuse any part.

---

## 🙏 Acknowledgements

- [MIT Indoor67 dataset](http://web.mit.edu/torralba/www/indoor67.html)
- [Places365](http://places2.csail.mit.edu/) for scene classification inspiration
- [Gradio](https://gradio.app) and [Hugging Face](https://huggingface.co) for excellent tools

---

## ✨ Future Improvements

- Support more design styles (Industrial, Scandinavian, Bohemian)
- Add real‑time webcam capture
- Integrate with furniture e‑commerce APIs

---

## 📬 Contact

For questions or issues, please open an issue on this repository or contact the team via your university email.
