import os
import sys
from core.feature_extraction import FeatureExtraction
from core.fastenerguidelines import FastenerGuideline
from core.agent import FastenerAgent

def main(image_path_2d, depth_image_path_3d):
    """Main function to process images and recommend fasteners"""
    try:
        # Validate file paths
        if not os.path.exists(image_path_2d):
            raise FileNotFoundError(f"2D image not found: {image_path_2d}")
        if not os.path.exists(depth_image_path_3d):
            raise FileNotFoundError(f"3D depth image not found: {depth_image_path_3d}")

        # Step 1: Extract features
        feature_extractor = FeatureExtraction(image_path_2d, depth_image_path_3d)
        features = feature_extractor.extract_features()

        # Step 2: Load Fastener Guidelines
        fastener_guideline = FastenerGuideline().get_guideline()  # FIXED this line

        # Step 3: Get fastener recommendation
        agent = FastenerAgent(fastener_guideline)
        fastener_decision = agent.find_best_fastener(features)

        return features, fastener_decision

    except Exception as e:
        print(f"Error in main process: {str(e)}", file=sys.stderr)
        return {}, {"fastener_type": "error", "explanation": str(e)}

if __name__ == "__main__":
    # Use raw strings for Windows paths and verify these paths exist
    BASE_DIR = r"E:\Feature extraciton"
    
    # Example images (verify these files exist)
    image_path_2d = os.path.join(BASE_DIR, "Screenshot_2025-02-07_102305.png")
    depth_image_path_3d = os.path.join(BASE_DIR, "Screenshot_2025-02-07_102945.png")

    # Run main process
    features, fastener_decision = main(image_path_2d, depth_image_path_3d)
    
    # Print formatted output
    print("\nExtraction Results:")
    for key, value in features.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\nRecommendation:")
    print(f"Fastener Type: {fastener_decision.get('fastener_type', 'Unknown')}")
    print(f"Reason: {fastener_decision.get('explanation', 'No explanation available')}")
