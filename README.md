# 🌿 AI powered plant disease detection system

An advanced, end-to-end Machine Learning pipeline and "Real RAG" application for agricultural disease detection. This system is designed as an academic Major Project to solve the "Lab vs. Field" domain adaptation problem using a custom Convolutional Neural Network (CNN) architecture.

## 👥 Project Team & Roles

| Name | Roll Number | Primary Responsibility |
| :--- | :--- | :--- |
| **Aman Kumar Bind** | `2201086CS` | **ML Architect** (Custom CNN, Mixed-Domain Training) |
| **Ankit Kumar Patel** | `2201116CS` | **Backend Engineer** (FastAPI, PostgreSQL, Auth Flow) |
| **Sahil Morwal** | `2201085CS` | **AI Integration Lead** (LangChain, FAISS, Real RAG System) |
| **Nawazish Hassan** | `2201031CS` | **Frontend & UI Architect** (Next.js, Glassmorphism, PDF Reports) |

## 🏆 Project Achievements (What is Done)

### 1. Custom CNN Architecture ("AgriNet")
Instead of using off-the-shelf models like ResNet or EfficientNet, we built a custom architecture from scratch using **Depthwise Separable Convolutions** and **Inverted Residual Blocks**.
- **Result:** Blazing fast inference speeds (perfect for mobile farming apps) while maintaining top-tier accuracy.

### 2. High-Accuracy Base Model
- Trained on **PlantVillage** (54,000+ clean lab images).
- Achieved **98.75% Validation Accuracy** across 38 distinct plant/disease classes.
- Used Adam optimizer and ReduceLROnPlateau scheduling to perfectly navigate the loss landscape.

### 3. "Mixed-Domain" Fine-Tuning (Real-World Robustness)
Laboratory conditions (PlantVillage) fail in the real world due to shadows, dirt, and messy backgrounds. To solve this, we used **Domain Adaptation**.
- Mapped 27 real-world field classes from the **PlantDoc** dataset to our standard 38 classes.
- Implemented `mixed_finetune_agrinet.py` to jointly train the base model on both clean lab data and messy field data simultaneously.
- **Pivotal Result:** Achieved **96.1% Validation Accuracy** in rigorous mixed-domain testing. 
- *The trained models are located in `ml-training/models/` and are fully tracked.*
- *The immense 3GB+ image datasets have been appropriately `.gitignore`d to maintain a clean repository.*

## 🚀 Roadmap (What is Left)

The Machine Learning architecture is officially complete and proven. We are now moving into the Full-Stack and Intelligence phases.

### 1. ⚙️ Core Backend (FastAPI + PostgreSQL)
- **Objective**: Move off local memory to a robust database.
- **Features**: JWT User Authentication, user profiles (`users` table), and prediction history logging (`predictions` table).

### 2. 📚 Knowledge-Grounded AI ("Real RAG")
- **Objective**: Upgrade from a generic chatbot to an academic **Retrieval-Augmented Generation** assistant.
- **Features**: Implement `LangChain` and `FAISS` vector databases to ingest heavy agricultural treatment PDFs. When a disease is detected, the AI will pull verified treatment remedies directly from the manuals.

### 3. ✨ Frontend Redesign (Premium Glassmorphism)
- **Objective**: Upgrade the UI/UX from a basic tool to a "Major Project"-worthy premium application.
- **Features**: Interactive, semi-transparent overlays, Framer Motion animations, and Grad-CAM "Heatmap" displays so the farmer sees *why* the AI made its prediction.

## 🛠️ How to Verify the ML Results
You can verify the robust accuracy of the custom model by running the evaluation scripts provided:

```powershell
# 1. Generate the official 38-class Confusion Matrix & Classification Report
python ml-training/evaluate_agrinet.py

# 2. View a visual grid testing the model strictly on messy field data (PlantDoc)
python ml-training/test_field_data.py
```
