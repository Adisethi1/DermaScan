import streamlit as st
import requests
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="HAM10000 Skin Lesion Analyzer", 
    page_icon="🔬",
    layout="centered"
)

st.title("🔬 Skin Lesion Classification Dashboard")
st.write("Upload a dermoscopic image from the HAM10000 dataset to analyze it using the trained CNN model.")

# Live Backend API Endpoint on Render
BACKEND_URL = "https://dermascan-ospu.onrender.com/predict"

# File Uploader Widget
uploaded_file = st.file_uploader(
    "Choose a skin lesion image file...", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image Scan Profile", use_column_width=True)
    
    # Analysis Trigger Button
    if st.button("Analyze Image", type="primary"):
        with st.spinner("Processing image through CNN classification pipeline..."):
            
            # Reset file pointer to the beginning of the buffer
            uploaded_file.seek(0)
            
            # Format payload for Flask multi-part upload
            files = {
                "file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)
            }
            
            try:
                # Send POST request to live Render API
                response = requests.post(BACKEND_URL, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Analysis Complete!")
                    
                    # Display metrics for classification and confidence scores
                    st.metric(
                        label="Detected Structural Classification", 
                        value=result.get('prediction', 'Unknown')
                    )
                    st.metric(
                        label="Model Algorithmic Certainty (Confidence)", 
                        value=result.get('confidence', 'N/A')
                    )
                    
                else:
                    st.error(f"Error returned from backend API pipeline: Code {response.status_code}")
                    if "error" in response.json():
                        st.caption(f"Details: {response.json()['error']}")
                        
            except requests.exceptions.ConnectionError:
                st.error("Could not reach backend API server.")
                st.info("💡 Ensure your Render backend service is live and active.")
