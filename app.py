import streamlit as st
import os
import tempfile
import logging
from PIL import Image
from main import main
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_image(uploaded_file):
    """
    Validate uploaded image file for size, format, and dimensions
    Returns: bool, error_message (if any)
    """
    try:
        if uploaded_file is None:
            return False, "No file uploaded"
        
        # Check file size (max 5MB)
        if uploaded_file.size > 5 * 1024 * 1024:
            return False, f"File {uploaded_file.name} is too large. Maximum size is 5MB"
        
        # Check file type
        allowed_types = ['image/jpeg', 'image/png']
        if uploaded_file.type not in allowed_types:
            return False, f"File {uploaded_file.name} must be PNG or JPEG format"
            
        # Verify image can be opened and check dimensions
        img = Image.open(uploaded_file)
        max_dimension = 2000
        if img.width > max_dimension or img.height > max_dimension:
            return False, f"Image dimensions must be under {max_dimension}x{max_dimension} pixels"
        
        # Reset file pointer after verification
        uploaded_file.seek(0)
        return True, None
        
    except Exception as e:
        logger.error(f"Image validation error for {uploaded_file.name}: {str(e)}")
        return False, f"Invalid image file: {str(e)}"

def save_uploaded_file(uploaded_file, temp_dir):
    """
    Save uploaded file to temporary directory
    Returns: file_path or None if error
    """
    try:
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        file_path = os.path.join(temp_dir, uploaded_file.name)
        uploaded_file.seek(0)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Failed to save file to {file_path}")
            
        logger.info(f"Successfully saved file to {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error saving file {uploaded_file.name}: {str(e)}")
        return None

def display_feature_details(features):
    """Display feature details in a formatted way"""
    try:
        st.write("### Geometry Details")
        
        # Create three columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Hole Depth", f"{features.get('hole_depth', 0):.2f} mm")
        with col2:
            st.metric("Hole Diameter", f"{features.get('hole_diameter', 0):.2f} mm")
        with col3:
            st.metric("Geometry Type", features.get('geometry_type', 'unknown'))
        
        # Show additional features if present
        if 'class_names' in features and features['class_names']:
            st.write("### Detected Objects")
            for class_name in features['class_names']:
                st.write(f"- {class_name}")
                
    except Exception as e:
        logger.error(f"Error displaying features: {str(e)}")
        st.error("Error displaying feature details")

def main_ui():
    """Main UI function for the Streamlit app"""
    try:
        st.set_page_config(
            page_title="Fastener Recommender",
            page_icon="🔩",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for better styling
        st.markdown("""
            <style>
            .main {
                background-color: #f0f2f6;
                padding: 2rem;
            }
            .stButton>button {
                width: 100%;
            }
            .upload-text {
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 1rem;
            }
            .results-container {
                padding: 1.5rem;
                border-radius: 0.5rem;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .metric-card {
                padding: 1rem;
                border-radius: 0.3rem;
                background-color: #f8f9fa;
                margin-bottom: 1rem;
            }
            </style>
        """, unsafe_allow_html=True)

        # Header
        st.title("🔩 AI Fastener Recommendation System")
        st.markdown("""
            This system analyzes your geometry and recommends the most suitable fastener.
            Upload both 2D and depth images to get started.
        """)

        # Sidebar configuration
        with st.sidebar:
            st.header("📤 Upload Images")
            
            img_2d = st.file_uploader(
                "2D Image (PNG/JPG)",
                type=["png", "jpg", "jpeg"],
                help="Upload a clear front view of your geometry"
            )
            
            img_3d = st.file_uploader(
                "3D Depth Image (PNG)",
                type=["png"],
                help="Upload a depth map image of your geometry"
            )
            
            st.markdown("---")
            
            with st.expander("ℹ️ Usage Guidelines", expanded=True):
                st.markdown("""
                    - Images should be clear and well-lit
                    - Maximum file size: 5MB
                    - Maximum dimensions: 2000x2000 pixels
                    - Supported formats: PNG, JPG
                    - Depth image should contain valid depth data
                """)

        # Main content area
        if img_2d and img_3d:
            # Validate images
            valid_2d, error_2d = validate_image(img_2d)
            valid_3d, error_3d = validate_image(img_3d)
            
            if not (valid_2d and valid_3d):
                if not valid_2d:
                    st.error(error_2d)
                if not valid_3d:
                    st.error(error_3d)
                return

            with tempfile.TemporaryDirectory() as temp_dir:
                # Save uploaded files
                img_2d_path = save_uploaded_file(img_2d, temp_dir)
                img_3d_path = save_uploaded_file(img_3d, temp_dir)
                
                if not (img_2d_path and img_3d_path):
                    st.error("Error saving uploaded files")
                    return

                # Display image previews
                st.write("### 📸 Image Previews")
                try:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(
                            img_2d,
                            caption="2D Geometry",
                            use_container_width=True
                        )
                    with col2:
                        st.image(
                            img_3d,
                            caption="Depth Map",
                            use_container_width=True
                        )
                except Exception as e:
                    logger.error(f"Error displaying images: {str(e)}")
                    st.error("Error displaying image previews")
                    return

                # Process images
                with st.spinner("🔄 Analyzing geometry..."):
                    try:
                        features, decision = main(img_2d_path, img_3d_path)
                        
                        if not features or not decision:
                            st.error("Analysis returned empty results")
                            return
                        
                        # Results section
                        st.markdown("---")
                        st.write("## 📊 Analysis Results")
                        
                        # Display extracted features
                        with st.expander("View Detailed Features", expanded=True):
                            if isinstance(features, dict):
                                display_feature_details(features)
                            else:
                                st.error("Invalid features format returned from analysis")
                                return
                        
                        # Display recommendation
                        st.markdown("---")
                        st.write("## 🎯 Fastener Recommendation")
                        
                        recommendation_cols = st.columns([2, 3])
                        with recommendation_cols[0]:
                            st.metric(
                                "Recommended Fastener",
                                decision.get("fastener_type", "Unknown").replace("_", " ").title()
                            )
                        
                        with recommendation_cols[1]:
                            explanation = decision.get('explanation', 'No explanation available')
                            st.info(f"**Reasoning:** {explanation}")
                        
                        # Status indicator
                        if "error" in decision.get("fastener_type", "").lower():
                            st.error("⚠️ Processing error occurred", icon="⚠️")
                        elif "unknown" in decision.get("fastener_type", "").lower():
                            st.warning("⚠️ No clear match found", icon="⚠️")
                        else:
                            st.success("✅ High confidence recommendation", icon="✅")
                            
                    except Exception as e:
                        logger.error(f"Error in analysis: {str(e)}")
                        st.error("❌ Processing Error")
                        with st.expander("View Error Details"):
                            st.exception(e)
        else:
            # Initial state
            st.info("👈 Please upload both images in the sidebar to begin analysis")

    except Exception as e:
        logger.error(f"Main UI error: {str(e)}")
        st.error("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    main_ui()