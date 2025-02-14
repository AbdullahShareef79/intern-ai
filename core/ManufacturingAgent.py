import os
import sys
import streamlit as st
from core.feature_extraction import FeatureExtraction
from core.fastenerguidelines import FastenerGuideline
from core.agent import FastenerAgent
import docx

class ManufacturingAgent:
    def __init__(self, manual_path):
        """Initialize the Manufacturing Agent with manufacturing guidelines from a manual."""
        self.guidelines = self.load_guidelines(manual_path)

    def load_guidelines(self, manual_path):
        """Loads manufacturing guidelines from a DOCX manual."""
        guidelines = {}
        try:
            doc = docx.Document(manual_path)
            for para in doc.paragraphs:
                if "-" in para.text:
                    key, value = para.text.split("-", 1)
                    guidelines[key.strip()] = value.strip()
        except Exception as e:
            print(f"Error loading manufacturing manual: {str(e)}")
        return guidelines

    def find_best_machine(self, features):
        """Determine the best manufacturing process based on extracted features."""
        hole_diameter = features.get("hole_diameter", 0)
        curvature = features.get("curvature", 0)
        geometry_type = features.get("geometry_type", "unknown")

        # Machine selection logic based on features
        if geometry_type == "flat" and hole_diameter > 10:
            machine = "Laser Cutting or Waterjet Cutting"
        elif geometry_type == "cylindrical":
            machine = "CNC Lathe or CNC Turning"
        elif geometry_type == "complex":
            machine = "CNC Milling or 5-Axis Machining"
        elif hole_diameter < 5:
            machine = "EDM (Electrical Discharge Machining)"
        else:
            machine = "3D Printing or Injection Molding"

        reason = self.guidelines.get(machine, "Default machine recommendation based on part geometry.")
        return {"machine": machine, "reason": reason}

def main(image_path_2d, depth_image_path_3d, manual_path):
    """Main function to process images and recommend fasteners and manufacturing processes."""
    try:
        if not os.path.exists(image_path_2d):
            raise FileNotFoundError(f"2D image not found: {image_path_2d}")
        if not os.path.exists(depth_image_path_3d):
            raise FileNotFoundError(f"3D depth image not found: {depth_image_path_3d}")

        # Step 1: Extract features
        feature_extractor = FeatureExtraction(image_path_2d, depth_image_path_3d)
        features = feature_extractor.extract_features()

        # Step 2: Load Fastener Guidelines
        fastener_guideline = FastenerGuideline().get_guideline()

        # Step 3: Get fastener recommendation
        agent = FastenerAgent(fastener_guideline)
        fastener_decision = agent.find_best_fastener(features)

        # Step 4: Get manufacturing recommendation
        manufacturing_agent = ManufacturingAgent(manual_path)
        manufacturing_decision = manufacturing_agent.find_best_machine(features)

        return features, fastener_decision, manufacturing_decision

    except Exception as e:
        print(f"Error in main process: {str(e)}", file=sys.stderr)
        return {}, {"fastener_type": "error", "explanation": str(e)}, {"machine": "error", "reason": str(e)}

if __name__ == "__main__":
    st.title("Fastener & Manufacturing Recommendation System")
    
    image_2d = st.file_uploader("Upload 2D Image", type=["png", "jpg", "jpeg"])
    depth_3d = st.file_uploader("Upload 3D Depth Image", type=["png", "jpg", "jpeg"])
    manual_path = "E:\\Feature extraciton\\Manufacturing Expert Manual.docx"
    
    if image_2d and depth_3d:
        temp_2d_path = "temp_2d.png"
        temp_3d_path = "temp_3d.png"
        
        with open(temp_2d_path, "wb") as f:
            f.write(image_2d.getbuffer())
        with open(temp_3d_path, "wb") as f:
            f.write(depth_3d.getbuffer())
        
        features, fastener_decision, manufacturing_decision = main(temp_2d_path, temp_3d_path, manual_path)
        
        st.subheader("Extracted Features")
        st.json(features)
        
        st.subheader("Recommended Fastener")
        st.write(f"**Type:** {fastener_decision.get('fastener_type', 'Unknown')}")
        st.write(f"**Reason:** {fastener_decision.get('explanation', 'No explanation available')}")
        
        st.subheader("Recommended Manufacturing Process")
        st.write(f"**Machine:** {manufacturing_decision.get('machine', 'Unknown')}")
        st.write(f"**Reason:** {manufacturing_decision.get('reason', 'No explanation available')}")
