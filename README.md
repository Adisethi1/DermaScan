Markdown
# 🩺 AI-Powered Skin Cancer Detection & Diagnostic Dashboard

 An enterprise-grade, full-stack medical computer vision system designed to assist dermatologists in non-invasive, multi-class skin lesion screening[cite: 1306].  Built on a decoupled two-tier MLOps architecture, this system processes dermoscopic imagery across 7 discrete pathological categories using the benchmark HAM10000 dataset[cite: 1321, 1483].

---

## 🌟 Key Engineering Features

-  **Brain (PyTorch + MobileNetV3 Small):** Fine-tuned convolutional neural network engineered for edge efficiency[cite: 1308, 1309].  Integrates custom **Inverse Frequency Class Weighting** into the Cross-Entropy Loss function to effectively eliminate majority-class bias (overcoming the 67% Melanocytic Nevi accuracy trap)[cite: 1330, 1332].
-  **Messenger (Flask REST API):** High-performance asynchronous API backend serving real-time model inferences[cite: 1312, 1314].  Converts multi-part binary image uploads into normalized $224 \times 224$ tensor matrices and outputs web-safe JSON diagnostic payloads[cite: 1317].
-  **Face (Streamlit Web Dashboard):** Interactive, doctor-facing web interface featuring secure session state authentication, live patient ID tracking, file drag-and-drop / camera input capture, and shift history logging[cite: 1318, 1320].

---

## 🔬 Detected Disease Categories (7 Classes)

1.  **MEL** — Melanoma (Malignant Pigment Cell Tumor) [cite: 1321, 1322]
2.  **BCC** — Basal Cell Carcinoma (Malignant Epithelial Cancer) [cite: 1323]
3.  **AKIEC** — Actinic Keratoses / Intraepithelial Carcinoma (Pre-cancerous) [cite: 1324]
4.  **BKL** — Benign Keratosis-like Lesions (Solar Lentigines / Seborrheic Keratoses) [cite: 1325]
5.  **NV** — Melanocytic Nevi (Standard Safe Everyday Moles) [cite: 1326]
6.  **DF** — Dermatofibroma (Harmless Cutaneous Nodules) [cite: 1328]
7.  **VASC** — Vascular Lesions (Cherry Angiomas & Superficial Blood Vessel Clusters) [cite: 1329]
