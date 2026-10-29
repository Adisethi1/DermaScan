# DermaScan — Clinical Skin Lesion Screening System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-MobileNetV3-EE4C2C.svg)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-green.svg)](https://flask.palletsprojects.com/)
[![HAM10000](https://img.shields.io/badge/Dataset-HAM10000-orange.svg)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

**DermaScan** is an AI-powered dermatological screening assistant designed to assist clinicians and researchers in classifying pigmented skin lesions across the 7 international diagnostic categories of the **HAM10000** benchmark.

Featuring a circular dermatoscope-inspired user interface, clinician authentication gateway, PyTorch MobileNetV3 deep learning engine, bio-optical ABCD feature analysis, and Grad-CAM region-of-interest explainability.

---

## 🔬 Key Features

* **Clinician Access Gateway**: Secure authentication requiring Clinician ID and password before granting access to screening tools.
* **Deep Learning Inference**: PyTorch MobileNetV3 deep convolutional backbone for dermatological feature extraction.
* **Bio-Optical Dermoscopic Analysis**: Evaluates Asymmetry, Border irregularity, Color variegation, and Diameter (ABCDE criteria), plus erythema, arborizing telangiectasia, fibrous hypopigmentation, and vascular lacunes.
* **7-Class HAM10000 Taxonomy**:
  1. `NV` — Melanocytic nevi (Benign mole)
  2. `MEL` — Melanoma (Malignant)
  3. `BCC` — Basal cell carcinoma (Malignant non-melanoma)
  4. `BKL` — Benign keratosis-like lesions (Seborrheic keratoses / Lentigines)
  5. `AKIEC` — Actinic keratoses / Intraepithelial carcinoma (Pre-malignant)
  6. `VASC` — Vascular lesions (Hemangiomas / Angiomas)
  7. `DF` — Dermatofibroma (Benign fibrous histiocytoma)
* **Explainable AI (XAI)**: Visual heatmap toggle simulating Grad-CAM region-of-interest focus to localize suspicious lesion regions.
* **1-Click Clinical Benchmark Samples**: Pre-loaded test samples for every single one of the 7 disease categories for instantaneous evaluation.
* **Diagnostic Breakdown & Confidence Dial**: Animated circular confidence ring and full probabilistic breakdown sorted by likelihood.

---

## 📁 Repository Structure

```text
dermaScan/
├── backend/
│   ├── main.py                     # Flask API & PyTorch inference server
│   └── ham10000_skin_model.pth     # Calibrated MobileNetV3 model weights
├── frontend/
│   ├── index.html                  # Clinician portal, dermatoscope UI & scripts
│   └── samples/                    # Verified clinical test sample images (7 classes)
│       ├── sample_nevus.jpg        # Melanocytic nevi (NV)
│       ├── sample_melanoma.jpg     # Melanoma (MEL)
│       ├── sample_bcc.jpg          # Basal cell carcinoma (BCC)
│       ├── sample_bkl.jpg          # Benign keratosis (BKL)
│       ├── sample_akiec.jpg        # Actinic keratosis (AKIEC)
│       ├── sample_vasc.jpg         # Vascular lesion (VASC)
│       └── sample_df.jpg           # Dermatofibroma (DF)
├── training/
│   └── train.ipynb                 # HAM10000 training & fine-tuning notebook
├── .gitignore                      # Git ignore rules
└── README.md                       # Documentation & instructions
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Dependencies

Ensure Python 3.9+ is installed. Install the required Python packages:

```bash
pip install torch torchvision flask pillow numpy opencv-python-headless
```

### 2. Launch the Application

From the project root directory, run the backend server:

```bash
python backend/main.py
```

The unified server will start on port `5001`:

```text
✅ Successfully loaded model weights from backend/ham10000_skin_model.pth
🚀 Starting DermaScan Secure Server on http://127.0.0.1:5001
```

### 3. Open in Browser

Navigate to:
👉 **[http://localhost:5001](http://localhost:5001)**

---

## 🔐 Authentication Credentials

The system comes pre-configured with the following clinician account:

| Field | Value |
| :--- | :--- |
| **Clinician ID** | `admin` |
| **Password** | `dermascan123` |

*(You can also click the **"Auto-fill & Log In"** button on the login screen for instant demo access).*

---

## 🧪 Testing the 7 Diagnostic Categories

Once logged in:
1. Under the circular dermatoscope aperture, click any of the **7 verified test sample pills**:
   * **Nevus (NV)**
   * **Melanoma (MEL)**
   * **Basal Cell (BCC)**
   * **Keratosis (BKL)**
   * **Actinic (AKIEC)**
   * **Vascular (VASC)**
   * **Fibroma (DF)**
2. Click **Analyze**.
3. View the **Confirmed Diagnosis**, **Confidence Score**, **7-Category Diagnostic Breakdown**, and **Clinical Findings**.
4. Toggle **Heatmap: on** to inspect the Grad-CAM region of interest.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the web application and clinician interface |
| `POST` | `/api/login` | Authenticates clinician credentials and generates session token |
| `POST` | `/api/logout` | Terminates active clinician session |
| `GET` | `/health` | Returns server health, active device (CPU/CUDA), and model status |
| `POST` | `/predict` | Multipart form endpoint taking `file` image and returning 7-class prediction JSON |

---

## ⚠️ Medical Disclaimer

**DermaScan is an academic research and screening-assistance system.** It is not an FDA-cleared or CE-marked medical device. All outputs produced by this system must be verified and interpreted by a licensed dermatologist, oncologist, or qualified healthcare professional before informing any clinical decisions or patient care.
