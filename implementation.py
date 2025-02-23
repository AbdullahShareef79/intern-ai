import json
import cv2
import numpy as np
from transformers import pipeline

# Load knowledge base
with open("structured_knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)

# Load Hugging Face LLM
try:
    generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
except:
    print("⚠️ Warning: Large model failed to load. Switching to a smaller model...")
    generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")  # Fallback to a smaller model

# Function to process image and detect shape
def process_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        raise FileNotFoundError(f"Error: Could not load image from {image_path}. Please check the file path.")
    
    # Apply edge detection
    edges = cv2.Canny(image, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return "No shape detected"

    shape_description = "Unknown shape"

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        num_sides = len(approx)

        if num_sides == 3:
            shape_description = "Triangular component"
        elif num_sides == 4:
            shape_description = "Rectangular or square component"
        elif num_sides > 5:
            shape_description = "Circular or complex component"
        else:
            shape_description = "Irregular geometry"

    return shape_description

# Function to get fastener and manufacturing recommendations
def get_recommendation_from_shape(shape_description):
    relevant_fasteners = list(knowledge_base["fasteners"].keys())  # Extract fastener names
    relevant_machines = list(knowledge_base["manufacturing_machines"].keys())  # Extract machine names

    prompt = f"""
You are an expert in mechanical engineering. Your task is to **select the best fastener and manufacturing process** for the given shape.

### **Component Details**
- **Detected Shape:** {shape_description}

### **Instructions**
1. Choose the **best fastener** for this shape from the following list:
   - Hex Head Screws
   - Socket Head Screws
   - Rounded Head Screws
   - Flat Head Screws
   - (Pick only ONE and provide a short reason)

2. Choose the **best manufacturing machine** for this shape from the following list:
   - CNC Milling
   - CNC Turning (Lathes)
   - Injection Molding
   - Laser Cutting & Waterjet Cutting
   - 3D Printing
   - Press Machines (Stamping & Forming)
   - (Pick only ONE and provide a short reason)

### **Answer Format (Strictly Follow This)**
DO NOT repeat the instructions. **Provide ONLY one complete answer, then STOP.**  

---
Fastener: Hex Head Screws  
Reason: Provides strong and durable fastening for circular components.  

Manufacturing Machine: CNC Milling  
Reason: Best for machining complex circular geometries.  
---

### **STOP GENERATING AFTER THIS. DO NOT CONTINUE.**
"""

    print("🚀 Sending prompt to LLM...")
    
    # Query the LLM
    response = generator(prompt, max_new_tokens=100, truncation=True)

    print("🔍 Raw LLM Output:", response)  # Debugging print

    # Extract useful content and ensure only the first valid answer is kept
    if isinstance(response, list) and len(response) > 0:
        response_text = response[0]["generated_text"] if "generated_text" in response[0] else response[0]["text"]
    else:
        response_text = "⚠️ Error: No valid response from the LLM."

    # Extract only the first valid response and ignore everything after
    response_lines = response_text.split("\n")
    clean_response = []
    for line in response_lines:
        if "Fastener:" in line or "Manufacturing Machine:" in line or "Reason:" in line:
            clean_response.append(line)
        if len(clean_response) == 4:  # Stop collecting after one complete answer
            break

    clean_response = "\n".join(clean_response)

    # Completely remove any extra content generated after the structured answer
    if "---" in clean_response:
        clean_response = clean_response.split("---")[0].strip()

    print("✅ AI Fastener & Manufacturing Recommendation:\n", clean_response)

    return clean_response

# Main execution
if __name__ == "__main__":
    image_path = "Sample Images/11.png"  # Use absolute path



    # Step 1: Detect shape
    shape_description = process_image(image_path)
    print(f"Detected Geometry: {shape_description}")

    # Step 2: Get fastener and manufacturing recommendation
    get_recommendation_from_shape(shape_description)  # Only print inside the function


