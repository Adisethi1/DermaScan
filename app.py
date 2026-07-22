import os
import io
import torch
import torch.nn as nn
from flask import Flask, request, jsonify
from torchvision import models, transforms
from PIL import Image

app = Flask(__name__)

# Alphabetical one-hot column mapping based on your GroundTruth.csv structure
DISEASE_CLASSES = {
    0: "Actinic keratoses (AKIEC)",
    1: "Basal cell carcinoma (BCC)",
    2: "Benign keratosis-like lesions (BKL)",
    3: "Dermatofibroma (DF)",
    4: "Melanoma (MEL) - Malignant",
    5: "Melanocytic nevi (NV) - Benign Mole",
    6: "Vascular lesions (VASC)"
}

# 1. Initialize the exact 7-class MobileNetV3 architecture used during training
device = torch.device('cpu') # Running on CPU for backend request stability
model = models.mobilenet_v3_small(weights=None)
model.classifier[3] = nn.Linear(model.classifier[3].in_features, 7)

# 2. Dynamic path configuration to find your weights file safely
# 2. Notebook-safe path configuration to find your weights file
BASE_DIR = os.getcwd()  # Gets the exact folder your notebook is sitting in
model_path = os.path.join(BASE_DIR, 'ham10000_skin_model.pth')
# Check if model file exists before booting the server
if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path, map_location=device))
    print("🎯 Model weights 'ham10000_skin_model.pth' loaded successfully!")
else:
    print("⚠️ WARNING: 'ham10000_skin_model.pth' not found in this folder. Run your training code first to generate it.")

model.eval()

# 3. Input Image Transforms (Must match the validation transforms from your training script)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded in the request'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read image file bytes safely into PIL memory
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        # Preprocess image and add a batch dimension (B, C, H, W)
        tensor = transform(image).unsqueeze(0).to(device)
        
        # Run inference pipeline
        # Run inference pipeline
        with torch.no_grad():
            outputs = model(tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted_idx = torch.max(probabilities, 0)
            
        # Get matching disease tag name and calculate accuracy percentage
        prediction_text = DISEASE_CLASSES[predicted_idx.item()]
        confidence_score = confidence.item() * 100

        # FIXED HERE: Return the actual variables assigned above
        return jsonify({
            'prediction': prediction_text,  
            'confidence': f"{confidence_score:.2f}%"
        })
        
    except Exception as e:
        return jsonify({'error': f"Processing error: {str(e)}"}), 500

if __name__ == '__main__':
    # Use environment port if available (for Render/Koyeb), else fallback to 5001
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
