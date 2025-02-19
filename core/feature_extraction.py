import cv2
import numpy as np
import pyvista as pv
from ultralytics import YOLO


class FeatureExtraction:
    def __init__(self, image_path_2d, depth_image_path_3d, model_path="yolov5su.pt"):
        """
        Initialize the FeatureExtraction class with paths to 2D and 3D images.

        Args:
            image_path_2d (str): Path to the 2D image.
            depth_image_path_3d (str): Path to the 3D depth image.
            model_path (str): Path to the YOLO model weights (default: "yolov5su.pt").
        """
        self.image_path_2d = image_path_2d
        self.depth_image_path_3d = depth_image_path_3d
        self.model = YOLO(model_path)  # Load YOLOv5 model
        self.image = self.load_image(self.image_path_2d)
        self.depth_image = self.load_depth_image(self.depth_image_path_3d)

    def load_image(self, path):
        """Load and validate a standard 2D image."""
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Error: Unable to load image at {path}")
        return image

    def load_depth_image(self, path):
        """Load and validate a 3D depth image."""
        depth_image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if depth_image is None:
            raise ValueError(f"Error: Unable to load depth image at {path}")
        return depth_image.astype(np.float32)

    def run_detection(self):
        """
        Run object detection on the 2D image using YOLO.

        Returns:
            results: YOLO detection results.
        """
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        results = self.model(image_rgb)
        return results

    def extract_2d_features(self):
        """
        Extract features from the 2D image using YOLO.

        Returns:
            features (dict): Extracted 2D features (bounding boxes, class names).
        """
        results = self.run_detection()
        features = {"bounding_boxes": [], "class_names": []}

        # Extract bounding box and class information
        for box in results[0].boxes:
            features['bounding_boxes'].append(box.xywh.tolist())  # Convert tensor to list
            features['class_names'].append(results[0].names[int(box.cls)])

        return features

    def extract_3d_features(self):
        """
        Extract features from the 3D depth image.

        Returns:
            features (dict): Extracted 3D features (hole diameter, hole depth, geometry type).
        """
        features = {}
        
        # Downscale the depth map for efficient processing
        scale_factor = 0.1
        depth_resized = cv2.resize(self.depth_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

        # Compute hole depth and diameter
        hole_depth = np.min(depth_resized)
        hole_diameter = np.max(depth_resized) - hole_depth

        # Validate hole depth and diameter
        if hole_depth < 0 or hole_diameter < 0:
            raise ValueError("Invalid depth data: Negative values detected.")

        features['hole_depth'] = round(hole_depth, 2)
        features['hole_diameter'] = round(hole_diameter, 2)

        # Infer geometry type based on depth variation
        features['geometry_type'] = "flat" if np.mean(depth_resized) > 0.5 else "rounded"

        return features

    def extract_features(self):
        """
        Extract both 2D and 3D features and combine them.

        Returns:
            all_features (dict): Combined 2D and 3D features.
        """
        # Extract 2D and 3D features
        features_2d = self.extract_2d_features()
        features_3d = self.extract_3d_features()

        # Merge both feature sets
        all_features = {**features_2d, **features_3d}

        # Ensure required 3D keys exist
        for key in ['hole_diameter', 'hole_depth', 'geometry_type']:
            all_features.setdefault(key, 'unknown')

        return all_features


# Example Usage:
if __name__ == "__main__":
    image_path_2d = "E:/Feature extraciton/intern-ai/Sample Images/Screenshot 2025-02-07 102945.png"  # Replace with actual 2D image path
    depth_image_path_3d = "E:/Feature extraciton/intern-ai/Sample Images/Screenshot 2025-02-07 102305.png"  # Replace with actual 3D depth image path

    extractor = FeatureExtraction(image_path_2d, depth_image_path_3d)
    features = extractor.extract_features()
    print(features)
