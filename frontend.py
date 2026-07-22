import streamlit as st
import requests
from PIL import Image
import io

# Page Configuration for a clean, medical-dashboard look
st.set_page_config(
    page_title="HAM10000 Skin Lesion Analyzer", 
    page_icon="🔬",
    layout="centered"
)

st.title("🔬 Skin Lesion Classification Dashboard")
st.write("Upload a dermoscopic image from the HAM10000 dataset to analyze it using the trained CNN model.")

# Target URL pointing to your backend Flask API running on port 5001
BACKEND_URL = "https://dermascan-ospu.onrender.com"
response = requests.post(BACKEND_URL, files={"file": uploaded_file.getvalue()})
# File Uploader Widget
uploaded_file = st.file_uploader(
    "Choose a skin lesion image file...", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Open and display the uploaded image to the user
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image Scan Profile", use_container_width=True)
    
    # Analysis Trigger Button
    if st.button("Analyze Image"):
        with st.spinner("Processing image through CNN classification pipeline..."):
            
            # Reset file pointer to the beginning of the file buffer
            uploaded_file.seek(0)
            
            # Format the file correctly for the requests multi-part form payload
            files = {
                "file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)
            }
            
            try:
                # Send the POST request to the Flask backend API
                response = requests.post(API_URL, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Analysis Complete!")
                    
                    # Display metrics for the classification and confidence scores
                    st.metric(
                        label="Detected Structural Classification", 
                        value=result['prediction']
                    )
                    st.metric(
                        label="Model Algorithmic Certainty (Confidence)", 
                        value=result['confidence']
                    )
                    
                else:
                    st.error(f"Error returned from backend API pipeline: Code {response.status_code}")
                    if "error" in response.json():
                        st.caption(f"Details: {response.json()['error']}")
                        
            except requests.exceptions.ConnectionError:
                st.error("Could not reach backend API server.")
                st.info("💡 Make sure your backend notebook cell or `app.py` script is actively running on http://127.0.0.1:5001 before clicking analyze.")
