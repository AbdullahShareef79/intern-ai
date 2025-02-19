Here’s your updated README with the **Streamlit** command added:  

---

# **Manufacturing Fastener & Machine Selection AI**

## 📌 **Overview**
This project is an **AI-powered manufacturing assistant** that helps identify the best fastener and manufacturing process for a given part. It takes an image (2D or 3D) as input, extracts key geometric features, and suggests:

- 🔩 **The best fastener type** based on predefined guidelines.  
- 🏭 **The most suitable manufacturing process** considering geometry and design constraints.  

---

## 🚀 **How It Works**
1️⃣ **Feature Extraction** 📸  
   - Extracts part features from 2D images and depth images (3D data).  

2️⃣ **Fastener Selection** 🔩  
   - Uses predefined engineering guidelines to determine the best fastener for the part.  

3️⃣ **Manufacturing Process Selection** 🏭  
   - Matches the extracted part features to an optimal manufacturing process based on expert knowledge.  

---

## 🛠 **Setup & Installation**
### **1️⃣ Install Dependencies**
Ensure you have **Python 3.13+** installed, then install the required dependencies:  
```sh
pip install -r requirements.txt
```

### **2️⃣ Run the Application**
You can run the application in two ways:

#### **▶️ Command Line Execution**
Execute the main script with:  
```sh
python main.py <image_2d_path> <depth_image_3d_path>
```
Example:  
```sh
python main.py sample_part.jpg sample_depth.png
```

#### **🌐 Streamlit Web App**
You can also run the application with a **user-friendly UI** using **Streamlit**:  
```sh
streamlit run app.py
```

---

## 🔍 **How the Decisions Are Made**
### 📌 **Fastener Selection**
- Uses a predefined guideline document (`Manufacturing Expert Manual.docx`).  
- The AI selects the best fastener based on hole size, material, and geometry.  

### 📌 **Manufacturing Process Selection**
- Based on extracted features like:  
  - **Hole diameter**  
  - **Curvature**  
  - **Geometry type** (flat, cylindrical, complex, etc.)  
- The AI recommends one of the following:  
  - **Laser Cutting / Waterjet Cutting**  
  - **CNC Machining / 5-Axis Milling**  
  - **3D Printing / Injection Molding**  
  - **EDM (Electrical Discharge Machining)**  

---

## 🏆 **Why This Matters**
✅ **Saves Engineering Time** ⏳  
✅ **Automates Decision Making** 🤖  
✅ **Optimizes Manufacturing Costs** 💰  

---

## 📬 **Get in Touch**
For any queries or contributions, feel free to reach out!  

📧 **Email**: abdullahshareef7945512@gmail.com  

💡 **Happy Manufacturing!** 🏭🚀  

