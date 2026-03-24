# AgriVision 2.0: Major Project Academic Checklist

Use this checklist to ensure your project meets the "Major Project" standards for your institution and instructor.

## 🔬 Research & Data
- [ ] **Literature Review**: Document 3-5 recent papers on CNNs or Vision Transformers for plant disease.
- [ ] **Dataset Merging**: Successfully combined PlantVillage, PlantDoc, and field images.
- [ ] **Class Balance Analysis**: Create a bar chart showing the distribution of images per class.

## 🤖 Model Implementation (AgriNet)
- [ ] **From Scratch Architecture**: Define and instantiate `AgriNet` in PyTorch (no `torchvision.models` pre-trained).
- [ ] **Custom Training Loop**: Implement a loop with:
  - Validation-based Early Stopping.
  - Learning Rate Scheduler (ReduceLROnPlateau).
  - WandB or TensorBoard tracking (highly recommended for major projects).
- [ ] **Explainability**: Generate and save Grad-CAM heatmaps for at least 10 different diseases.

## ⚙️ System Features
- [ ] **Robust Database**: PostgreSQL or MySQL for storing prediction history.
- [ ] **User Auth**: Secure login/signup flow with JWT.
- [ ] **Real RAG Integration**: Custom knowledge retrieval from agricultural manuals.
- [ ] **Aesthetics**: Glassmorphism UI with Framer Motion animations.
- [ ] **Reporting**: Automated PDF generation for results.

## 🧪 Documentation & Testing
- [ ] **Confusion Matrix**: Generate a matrix showing where the model gets confused.
- [ ] **Performance Report**: Compare AgriNet results with your old EfficientNet-B0 model.
- [ ] **Final Report**: 50+ page document covering:
  - Abstract & Problem Statement.
  - Proposed Architecture (AgriNet).
  - Dataset Preparation.
  - Results & Discussion.
  - Future Work.

## 💡 Pro-Tip for Major Projects
If you have time, add **"Pest Detection"** or **"Leaf Condition Analysis"** (detecting drought/nutrient deficiencies) as a secondary model. This adds significant "Major Project" value.
