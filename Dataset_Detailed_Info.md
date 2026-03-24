# AgriVision 2.0: Dataset Deep Dive

To make your project "Major," you need to bridge the gap between Lab and Field. These are the three core datasets suggested in your roadmap.

## 1. PlantVillage (The Foundation)
- **Source**: Penn State University.
- **Scale**: ~54,306 images across 38 classes (14 plant species).
- **Style**: **Controlled/Laboratory**. Leaves are placing on a uniform grey background.
- **Why it matters**: It's the most comprehensive set for "Disease Identity." It gives your model the best initial understanding of what a "spot" or "blight" looks like.
- **Limitation**: Direct training on *only* this lead to "overfitting" on the grey background. The model might fail in a real field.

## 2. PlantDoc (The Real World)
- **Source**: Indian Institute of Technology (IIT).
- **Scale**: ~2,598 images across 13 species.
- **Style**: **Field/In-the-wild**. These are images of plants in actual farms, with soil, sunlight, insects, and other leaves in the background.
- **Why it matters**: It teaches your model to "ignore the noise." Combining this with PlantVillage is what makes a "Major Project" robust enough for actual farmers to use.

## 3. Plant Pathology 2021 (The Detail Enhancer)
- **Source**: Kaggle FGVC8 Competition.
- **Scale**: ~23,000 high-quality images.
- **Style**: **High-Resolution Expert Images**. Focused on Apple leaves.
- **Why it matters**: If you want to show "Specialization" in your project, this dataset allows you to deeply analyze one specific crop (Apple) with extreme precision. It's often used for "Multi-label classification" (e.g., a leaf having both Scab and Rust).

---

## 🛠️ How to use these together?
For your Major Project, I recommend a **Hybrid Dataset** approach:

1.  **Stage 1**: Train on **PlantVillage** to get the basic disease features.
2.  **Stage 2**: Fine-tune on a "Merged" dataset of **PlantDoc + subset of PlantVillage**.
3.  **Result**: A model that understands the disease but isn't confused by background dirt or shadows.

**Academic Tip**: In your report, mention that you used "Domain Adaptation" to move from laboratory images (PlantVillage) to real-world images (PlantDoc). Your instructor will be very impressed!
