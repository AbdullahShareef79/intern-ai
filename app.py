import streamlit as st
import os
import tempfile
import logging
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any
from PIL import Image
from pathlib import Path
from main import main

# Constants
MAX_FILE_SIZE_MB = 5
MAX_IMAGE_DIMENSION = 2000
ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png'}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")],
)
logger = logging.getLogger(__name__)

@dataclass
class ImageValidationResult:
    """Data class for image validation results"""
    is_valid: bool
    error_message: Optional[str] = None

@dataclass
class ProcessingResult:
    """Data class for processing results"""
    features: Dict[str, Any]
    fastener_decision: Dict[str, Any]
    manufacturing_decision: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None

class FastenerRecommenderUI:
    """Main UI class for the Fastener Recommender application"""

    def __init__(self):
        """Initialize the UI components"""
        self.setup_page_config()
        self.apply_custom_styles()

    @staticmethod
    def setup_page_config():
        """Configure the Streamlit page settings"""
        st.set_page_config(
            page_title="AI Fastener & Manufacturing Recommender",
            page_icon="🔩",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    @staticmethod
    def apply_custom_styles():
        """Apply custom CSS styles"""
        st.markdown(
            """
            <style>
            .main { background-color: #f5f7f9; padding: 2rem; }
            .stButton>button { width: 100%; background-color: #2e6de4; color: white; font-weight: bold; }
            .metric-container { background-color: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            .results-section { margin-top: 2rem; padding: 1.5rem; background-color: white; border-radius: 0.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            .recommendation-card { padding: 1rem; background-color: #f0f7ff; border-left: 4px solid #2e6de4; margin: 1rem 0; }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def render_sidebar(self) -> Tuple[Optional[Any], Optional[Any]]:
        """Render sidebar elements and return uploaded files"""
        with st.sidebar:
            st.header("📤 Upload Images")

            img_2d = st.file_uploader(
                "2D Image", type=["png", "jpg", "jpeg"], help="Upload a clear front view image"
            )

            img_3d = st.file_uploader(
                "Depth Image", type=["png"], help="Upload a depth map image"
            )

            st.markdown("---")

            with st.expander("📋 Guidelines", expanded=True):
                st.markdown(
                    """
                    #### Requirements:
                    - Clear, well-lit images
                    - Max size: 5MB per image
                    - Max dimensions: 2000x2000px
                    - Formats: PNG, JPG

                    #### Best Practices:
                    - Center the object in frame
                    - Ensure proper lighting
                    - Avoid shadows and reflections
                    - Use consistent scale
                    """
                )

        return img_2d, img_3d

    @staticmethod
    def display_metrics(features: Dict[str, Any]):
        """Display feature metrics in a formatted grid"""
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)

        cols = st.columns(3)
        metrics = [
            ("Hole Depth", f"{features.get('hole_depth', 0):.2f} mm"),
            ("Hole Diameter", f"{features.get('hole_diameter', 0):.2f} mm"),
            ("Geometry Type", features.get("geometry_type", "Unknown")),
        ]

        for col, (label, value) in zip(cols, metrics):
            with col:
                st.metric(label, value)

        if "class_names" in features and features["class_names"]:
            st.write("#### Detected Objects:")
            for class_name in features["class_names"]:
                st.markdown(f"- {class_name}")

        st.markdown("</div>", unsafe_allow_html=True)

    def process_images(self, img_2d_path: str, img_3d_path: str) -> ProcessingResult:
        """Process uploaded images and return results."""
        try:
            manual_path = "E:\\Feature extraciton\\Manufacturing Expert Manual.docx"
            features, fastener_decision, manufacturing_decision = main(
                img_2d_path, img_3d_path, manual_path
            )

            if not features or not fastener_decision or not manufacturing_decision:
                return ProcessingResult(
                    features={},
                    fastener_decision={},
                    manufacturing_decision={},
                    success=False,
                    error_message="Analysis returned empty results",
                )

            return ProcessingResult(
                features=features,
                fastener_decision=fastener_decision,
                manufacturing_decision=manufacturing_decision,
                success=True,
            )

        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            return ProcessingResult(
                features={},
                fastener_decision={},
                manufacturing_decision={},
                success=False,
                error_message=str(e),
            )

    def display_recommendation(self, decision: Dict[str, Any], title: str, icon: str):
        """Display recommendation with professional styling and structured layout."""

        # Map machines to icons
        machine_icons = {
            "Laser Cutting or Waterjet Cutting": "🔦",
            "CNC Lathe or CNC Turning": "⚙️",
            "CNC Milling or 5-Axis Machining": "🛠️",
            "EDM (Electrical Discharge Machining)": "⚡",
            "3D Printing or Injection Molding": "🖨️"
        }
        
        # Extract details
        machine = decision.get("machine", "Unknown")
        reason = decision.get("reason", "No explanation available")
        
        # Select appropriate icon
        machine_icon = machine_icons.get(machine, "🏭")  # Default factory icon
        
        # Apply enhanced CSS styles for a professional look
        st.markdown(f"""
            <div style="
                background-color: #eef6ff;
                padding: 15px;
                border-radius: 12px;
                border-left: 6px solid #2e6de4;
                font-size: 18px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            ">
                <b>{machine_icon} {title}</b> <br>
                <span style="font-size: 22px; font-weight: bold; color: #2e6de4;">{machine}</span> <br>
                <span style="color: #333;">📝 <i>{reason}</i></span>
            </div>
        """, unsafe_allow_html=True)

        # Display status indicators
        status = decision.get("machine", "").lower()
        if "error" in status:
            st.error("⚠️ Processing error occurred")
        elif "unknown" in status:
            st.warning("⚠️ No clear match found")
        else:
            st.success(f"✅ {title} Recommended", icon=icon)

    def run(self):
        """Main application loop."""
        try:
            st.title("🔩 AI Fastener & Manufacturing Recommendation System")
            st.markdown("Upload images to receive AI-powered fastener & manufacturing suggestions.")

            # Get uploaded files
            img_2d, img_3d = self.render_sidebar()

            if not (img_2d and img_3d):
                st.info("👈 Please upload both required images to begin analysis")
                return

            # Process images
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir = Path(temp_dir)

                # Save files
                img_paths = {"2D": temp_dir / img_2d.name, "3D": temp_dir / img_3d.name}
                for img_type, uploaded_file in {"2D": img_2d, "3D": img_3d}.items():
                    with open(img_paths[img_type], "wb") as f:
                        f.write(uploaded_file.getbuffer())

                # Process images
                with st.spinner("🔄 Analyzing geometry..."):
                    result = self.process_images(str(img_paths["2D"]), str(img_paths["3D"]))

                    if not result.success:
                        st.error(f"Analysis failed: {result.error_message}")
                        return

                    # Display results
                    st.markdown("## 📊 Analysis Results")
                    self.display_metrics(result.features)

                    st.markdown("## 🎯 Fastener Recommendation")
                    self.display_recommendation(result.fastener_decision, "🔩 Fastener Type", "✅")

                    st.markdown("## 🏭 Manufacturing Process")
                    self.display_recommendation(result.manufacturing_decision, "🏭 Manufacturing Process", "✅")

        except Exception as e:
            logger.error(f"Application error: {str(e)}")
            st.error("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    FastenerRecommenderUI().run()