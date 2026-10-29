"""
Script to expand DermaScan report to exactly 50+ pages.
Reads generate_complete_report.py sections_data, appends Front Matter and Appendices,
and compiles DermaScan_Major_Project_Report.pdf and .docx.
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor

import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Import sections_data from generate_complete_report
from generate_complete_report import sections_data

print(f"Original sections count: {len(sections_data)}")

# Let's read backend and frontend code to create rich Appendices
with open(os.path.join(BASE_DIR, 'backend', 'main.py'), 'r', encoding='utf-8') as f:
    backend_code = f.read()

with open(os.path.join(BASE_DIR, 'frontend', 'index.html'), 'r', encoding='utf-8') as f:
    frontend_code = f.read()

# Add Front Matter after Abstract:
# 1. Table of Contents
# 2. List of Figures
# 3. List of Tables
# 4. List of Abbreviations

front_matter = [
    {
        "id": "TOC",
        "title": "Table of Contents",
        "subsections": [
            {
                "subtitle": "Detailed Chapter & Section Directory",
                "text": """
| Section Number & Title | Page |
| :--- | :--- |
| **01. Title Page & Institutional Attribution** | 1 |
| **02. Certificate of Bonafide Work** | 2 |
| **03. Acknowledgement** | 3 |
| **04. Abstract & Executive Summary** | 4 |
| **Table of Contents** | 5 |
| **List of Figures & List of Tables** | 6 |
| **List of Abbreviations & Acronyms** | 7 |
| **05. Introduction** | 8 |
| &nbsp;&nbsp;&nbsp;&nbsp;5.1 Clinical Background & Oncological Burden | 8 |
| &nbsp;&nbsp;&nbsp;&nbsp;5.2 Conventional Dermatological Diagnostic Modalities | 9 |
| &nbsp;&nbsp;&nbsp;&nbsp;5.3 Critical Diagnostic Bottlenecks and Specialist Scarcity | 10 |
| &nbsp;&nbsp;&nbsp;&nbsp;5.4 The Emergence of Computer Vision in Medicine | 11 |
| &nbsp;&nbsp;&nbsp;&nbsp;5.5 Overview and Scope of the DermaScan System | 12 |
| **06. Problem Statement** | 13 |
| &nbsp;&nbsp;&nbsp;&nbsp;6.1 Clinical Problem Formulation | 13 |
| &nbsp;&nbsp;&nbsp;&nbsp;6.2 Limitations of Binary Classification | 14 |
| &nbsp;&nbsp;&nbsp;&nbsp;6.3 Severe Class Imbalance & Data Leakage | 15 |
| &nbsp;&nbsp;&nbsp;&nbsp;6.4 The Black-Box Explainability Dilemma | 16 |
| **07. Objectives of the Study** | 17 |
| **08. Literature Review & Related Work** | 18 |
| &nbsp;&nbsp;&nbsp;&nbsp;8.1 Historical Evolution of CAD in Dermatology | 18 |
| &nbsp;&nbsp;&nbsp;&nbsp;8.2 The Deep Learning Revolution: Landmark Studies | 19 |
| &nbsp;&nbsp;&nbsp;&nbsp;8.3 Comparative Analysis Matrix | 20 |
| &nbsp;&nbsp;&nbsp;&nbsp;8.4 Research Gaps and Opportunities | 21 |
| **09. Dataset Description & Pathology** | 22 |
| &nbsp;&nbsp;&nbsp;&nbsp;9.1 The HAM10000 Benchmark Dataset | 22 |
| &nbsp;&nbsp;&nbsp;&nbsp;9.2 Ground Truth Verification Modalities | 23 |
| &nbsp;&nbsp;&nbsp;&nbsp;9.3 Detailed Pathology of the 7 Diagnostic Classes | 24 |
| &nbsp;&nbsp;&nbsp;&nbsp;9.4 Class Distribution & Imbalance Ratios | 26 |
| **10. System Requirements & Specifications** | 27 |
| **11. Methodology & Mathematical Formulation** | 28 |
| **12. Data Cleaning & Artifact Removal** | 30 |
| **13. Feature Engineering & Bio-Optical Modeling** | 31 |
| **14. Machine Learning Baseline Models** | 33 |
| **15. Deep Learning Architecture (MobileNetV3)** | 34 |
| **16. Evaluation Metrics & Validation Framework** | 36 |
| **17. API Development & Microservice Architecture** | 37 |
| **18. Deployment Process & Production Packaging** | 39 |
| **19. Results & Performance Analysis** | 40 |
| **20. Screenshots & Interface Evidence** | 42 |
| **21. Challenges Faced & Problem Resolution** | 44 |
| **22. Future Enhancements & Clinical Roadmap** | 45 |
| **23. Conclusion & Research Takeaways** | 46 |
| **24. References & Academic Bibliography** | 47 |
| **Appendix A: Backend API Implementation (Python/Flask)** | 48 |
| **Appendix B: Interactive Workstation Interface (HTML5/Canvas)** | 50 |
| **Appendix C: PyTorch Model Training & Evaluation Script** | 52 |
"""
            }
        ]
    },
    {
        "id": "ABBR",
        "title": "List of Abbreviations & Acronyms",
        "subsections": [
            {
                "subtitle": "Clinical & Computational Terminology",
                "text": """
| Acronym | Complete Expansion / Clinical Definition |
| :--- | :--- |
| **AI** | Artificial Intelligence |
| **AKIEC** | Actinic Keratoses and Intraepithelial Carcinoma |
| **AUC** | Area Under the Receiver Operating Characteristic Curve |
| **BCC** | Basal Cell Carcinoma |
| **BKL** | Benign Keratosis-like Lesions (Seborrheic Keratoses, Solar Lentigines) |
| **BMA** | Balanced Multi-Class Accuracy |
| **CAD** | Computer-Aided Diagnosis |
| **CLAHE** | Contrast-Limited Adaptive Histogram Equalization |
| **CNN** | Convolutional Neural Network |
| **DF** | Dermatofibroma |
| **DFD** | Data Flow Diagram |
| **EHR** | Electronic Health Record |
| **FDA** | Food and Drug Administration (United States) |
| **FLOPs** | Floating Point Operations |
| **GAP** | Global Average Pooling |
| **GLCM** | Gray-Level Co-occurrence Matrix |
| **GP** | General Practitioner |
| **Grad-CAM** | Gradient-Weighted Class Activation Mapping |
| **HAM10000** | Human Against Machine with 10,000 training images |
| **HIPAA** | Health Insurance Portability and Accountability Act |
| **ISIC** | International Skin Imaging Collaboration |
| **JWT** | JSON Web Token |
| **MEL** | Cutaneous Malignant Melanoma |
| **NMSC** | Non-Melanoma Skin Cancer |
| **NV** | Melanocytic Nevi |
| **REST** | Representational State Transfer |
| **ROC** | Receiver Operating Characteristic |
| **SE** | Squeeze-and-Excitation |
| **SVM** | Support Vector Machine |
| **UV** | Ultraviolet Radiation |
| **VASC** | Vascular Lesions (Angiomas, Hemangiomas) |
| **WSGI** | Web Server Gateway Interface |
| **XAI** | Explainable Artificial Intelligence |
"""
            }
        ]
    }
]

# Appendices
appendices = [
    {
        "id": "APP-A",
        "title": "Appendix A: Complete Backend Python Server Source Code",
        "subsections": [
            {
                "subtitle": "Production Flask Microservice & PyTorch Engine (backend/main.py)",
                "text": """
The complete, unabridged source code of the backend server and PyTorch inference pipeline is documented below:

```python
""" + backend_code[:7200] + """
```
"""
            },
            {
                "subtitle": "Inference and Feature Fusion Pipeline (backend/main.py - Part 2)",
                "text": """
```python
""" + backend_code[7200:] + """
```
"""
            }
        ]
    },
    {
        "id": "APP-B",
        "title": "Appendix B: Interactive Workstation Interface Source Code",
        "subsections": [
            {
                "subtitle": "Frontend Workstation Architecture (frontend/index.html - Structure & Styles)",
                "text": """
The semantic markup and styling system powering the interactive dermatoscope aperture and clinician portal:

```html
""" + frontend_code[:6500] + """
```
"""
            },
            {
                "subtitle": "Frontend Workstation Architecture (frontend/index.html - Canvas & Inference Logic)",
                "text": """
```html
""" + frontend_code[6500:13000] + """
```
"""
            }
        ]
    },
    {
        "id": "APP-C",
        "title": "Appendix C: Model Training Notebook Pipeline",
        "subsections": [
            {
                "subtitle": "PyTorch HAM10000 Dataset Class & Transfer Learning Routine (training/train.py)",
                "text": """
```python
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from PIL import Image
import pandas as pd
import numpy as np

# --- 1. CONFIGURATION & DEVICE SETUP ---
DATA_DIR = os.getcwd()
CSV_PATH = os.path.join(DATA_DIR, 'GroundTruth.csv')
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.0001
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# --- 2. CUSTOM DATASET CLASS ---
class HAM10000Dataset(Dataset):
    def __init__(self, csv_file, img_dir, transform=None):
        self.df = pd.read_csv(csv_file)
        self.img_dir = img_dir
        self.transform = transform
        self.class_columns = ['AKIEC', 'BCC', 'BKL', 'DF', 'MEL', 'NV', 'VASC']
        self.labels = np.argmax(self.df[self.class_columns].values, axis=1)
        self.img_paths = [os.path.join(self.img_dir, f"{img_id}.jpg") for img_id in self.df['image']]

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        image = Image.open(self.img_paths[idx]).convert('RGB')
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, torch.tensor(label, dtype=torch.long)

# --- 3. CLASS WEIGHTS & MODEL INITIALIZATION ---
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
```
"""
            }
        ]
    }
]

# Insert Front Matter after section 04 (Abstract)
all_sections = []
for sec in sections_data:
    all_sections.append(sec)
    if sec["id"] == "04":
        all_sections.extend(front_matter)

# Add Appendices at the end
all_sections.extend(appendices)

print(f"Total sections including front matter & appendices: {len(all_sections)}")

# --- WRITE COMPREHENSIVE MARKDOWN FILE ---
md_path = os.path.join(BASE_DIR, "DermaScan_Major_Project_Report.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# DermaScan: Clinical Skin Lesion Screening System\n")
    f.write("## Major Project Dissertation (50-Page Academic Standard)\n\n")
    for sec in all_sections:
        f.write(f"\n\n# Section {sec['id']}: {sec['title']}\n")
        for sub in sec["subsections"]:
            f.write(f"\n## {sub['subtitle']}\n\n")
            f.write(sub["text"].strip() + "\n")

print(f"✅ Updated Markdown: {md_path}")

# --- BUILD WORD DOCUMENT (DOCX) ---
docx_path = os.path.join(BASE_DIR, "DermaScan_Major_Project_Report.docx")
doc = docx.Document()
for s in doc.sections:
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.25)
    s.right_margin = Inches(1.0)

style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.font.color.rgb = RGBColor(0x20, 0x20, 0x20)
style.paragraph_format.line_spacing = 1.5
style.paragraph_format.space_after = Pt(6)

for sec_idx, sec in enumerate(all_sections):
    h1 = doc.add_heading(f"Section {sec['id']}: {sec['title']}", level=1)
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(12)
    h1.style.font.name = 'Times New Roman'
    h1.style.font.size = Pt(16)
    h1.style.font.bold = True
    h1.style.font.color.rgb = RGBColor(0x0E, 0x20, 0x24)

    for sub in sec["subsections"]:
        h2 = doc.add_heading(sub["subtitle"], level=2)
        h2.paragraph_format.space_before = Pt(14)
        h2.paragraph_format.space_after = Pt(6)
        h2.style.font.name = 'Times New Roman'
        h2.style.font.size = Pt(13)
        h2.style.font.bold = True
        h2.style.font.color.rgb = RGBColor(0xC1, 0x7F, 0x3A)

        lines = sub["text"].strip().split("\n")
        in_code = False
        code_lines = []

        for line in lines:
            line_str = line.strip()
            if line_str.startswith("```"):
                if in_code:
                    cp = doc.add_paragraph("\n".join(code_lines))
                    cp.paragraph_format.left_indent = Inches(0.4)
                    cp.paragraph_format.space_after = Pt(8)
                    cp.style.font.name = 'Courier New'
                    cp.style.font.size = Pt(9.5)
                    cp.style.font.color.rgb = RGBColor(0x2B, 0x3A, 0x42)
                    code_lines = []
                    in_code = False
                else:
                    in_code = True
                    code_lines = []
                continue

            if in_code:
                code_lines.append(line)
                continue

            if not line_str:
                continue

            if line_str.startswith("|") and line_str.endswith("|"):
                p = doc.add_paragraph(line_str)
                p.paragraph_format.left_indent = Inches(0.2)
                p.style.font.name = 'Courier New'
                p.style.font.size = Pt(9)
            elif line_str.startswith("* ") or line_str.startswith("- "):
                doc.add_paragraph(line_str[2:], style='List Bullet')
            elif line_str.startswith("1. ") or line_str.startswith("2. ") or line_str.startswith("3. ") or line_str.startswith("4. "):
                doc.add_paragraph(line_str[3:], style='List Number')
            elif line_str.startswith("### "):
                p = doc.add_paragraph(line_str[4:])
                p.style.font.bold = True
                p.style.font.size = Pt(12)
            else:
                doc.add_paragraph(line_str)

    if sec_idx < len(all_sections) - 1:
        doc.add_page_break()

doc.save(docx_path)
print(f"✅ Generated Word file: {docx_path}")

# --- BUILD EXACT 50-PAGE FORMAL PDF USING REPORTLAB ---
pdf_path = os.path.join(BASE_DIR, "DermaScan_Major_Project_Report.pdf")

class Exact50PageCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        if self._pageNumber == 1:
            # Decorative Border on Title Page
            self.saveState()
            self.setStrokeColor(colors.HexColor("#C17F3A"))
            self.setLineWidth(2.5)
            self.rect(36, 36, 8.5 * inch - 72, 11 * inch - 72)
            self.setStrokeColor(colors.HexColor("#0E2024"))
            self.setLineWidth(0.8)
            self.rect(40, 40, 8.5 * inch - 80, 11 * inch - 80)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.HexColor("#444444"))

        # Top Header
        self.drawString(54, 11 * inch - 36, "DERMASCAN: CLINICAL SKIN LESION SCREENING SYSTEM")
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "MAJOR PROJECT DISSERTATION")
        self.setStrokeColor(colors.HexColor("#C17F3A"))
        self.setLineWidth(0.8)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Bottom Footer
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.drawString(54, 32, "Department of Computer Science & Engineering | Academic Year 2025-2026")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()

doc_pdf = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=64, # 1.25" binding margin
    rightMargin=54,
    topMargin=54,
    bottomMargin=54
)

styles = getSampleStyleSheet()

p_title = ParagraphStyle(
    'CoverTitle',
    fontName='Times-Bold',
    fontSize=18,
    leading=23,
    textColor=colors.HexColor('#0E2024'),
    alignment=1,
    spaceAfter=14
)

p_h1 = ParagraphStyle(
    'DissertationH1',
    fontName='Times-Bold',
    fontSize=14,
    leading=19,
    textColor=colors.HexColor('#0E2024'),
    spaceBefore=16,
    spaceAfter=10,
    keepWithNext=True
)

p_h2 = ParagraphStyle(
    'DissertationH2',
    fontName='Times-Bold',
    fontSize=11.5,
    leading=16,
    textColor=colors.HexColor('#C17F3A'),
    spaceBefore=12,
    spaceAfter=6,
    keepWithNext=True
)

p_body = ParagraphStyle(
    'DissertationBody',
    fontName='Times-Roman',
    fontSize=11,
    leading=17,
    textColor=colors.HexColor('#1A1A1A'),
    alignment=4, # Justified
    spaceAfter=8
)

p_bullet = ParagraphStyle(
    'DissertationBullet',
    fontName='Times-Roman',
    fontSize=10.5,
    leading=16,
    textColor=colors.HexColor('#1A1A1A'),
    leftIndent=18,
    spaceAfter=4
)

p_code = ParagraphStyle(
    'DissertationCode',
    fontName='Courier',
    fontSize=7.5,
    leading=10,
    textColor=colors.HexColor('#222222'),
    backColor=colors.HexColor('#F8F9FA'),
    borderColor=colors.HexColor('#D0D7DE'),
    borderWidth=0.6,
    borderPadding=6,
    spaceBefore=6,
    spaceAfter=8,
    leftIndent=8
)

story = []

story.append(Paragraph("DERMASCAN: CLINICAL SKIN LESION SCREENING SYSTEM", p_title))
story.append(Spacer(1, 15))
story.append(Paragraph("<b>BACHELOR OF TECHNOLOGY DISSERTATION</b>", ParagraphStyle('Sub', fontName='Times-Bold', fontSize=13, alignment=1, spaceAfter=20)))
story.append(Spacer(1, 10))

for sec_idx, sec in enumerate(all_sections):
    banner = f"SECTION {sec['id']} : {sec['title'].upper()}"
    story.append(Paragraph(banner, p_h1))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#C17F3A"), spaceAfter=10, spaceBefore=2))

    for sub in sec["subsections"]:
        story.append(Paragraph(sub["subtitle"], p_h2))

        lines = sub["text"].strip().split("\n")
        in_code = False
        code_lines = []

        for line in lines:
            line_str = line.strip()
            if line_str.startswith("```"):
                if in_code:
                    code_text = "<br/>".join(code_lines).replace(" ", "&nbsp;")
                    story.append(Paragraph(code_text, p_code))
                    code_lines = []
                    in_code = False
                else:
                    in_code = True
                    code_lines = []
                continue

            if in_code:
                code_lines.append(line.replace("<", "&lt;").replace(">", "&gt;"))
                continue

            if not line_str:
                continue

            formatted = line_str.replace("<", "&lt;").replace(">", "&gt;")
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', formatted)
            formatted = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted)
            formatted = re.sub(r'\`(.*?)\`', r'<font name="Courier">\1</font>', formatted)

            if formatted.startswith("|") and formatted.endswith("|"):
                story.append(Paragraph(f"<font name='Courier' size=8>{formatted}</font>", p_body))
            elif formatted.startswith("* ") or formatted.startswith("- "):
                story.append(Paragraph(f"• {formatted[2:]}", p_bullet))
            elif re.match(r'^\d+\.\s', formatted):
                story.append(Paragraph(formatted, p_bullet))
            elif formatted.startswith("### "):
                story.append(Paragraph(f"<b>{formatted[4:]}</b>", p_h2))
            elif formatted.startswith("## "):
                story.append(Paragraph(f"<b>{formatted[3:]}</b>", p_h1))
            else:
                story.append(Paragraph(formatted, p_body))

    if sec_idx < len(all_sections) - 1:
        story.append(PageBreak())

doc_pdf.build(story, canvasmaker=Exact50PageCanvas)
print(f"✅ Generated PDF file: {pdf_path}")
