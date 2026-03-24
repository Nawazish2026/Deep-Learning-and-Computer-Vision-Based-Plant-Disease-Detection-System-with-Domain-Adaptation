import torch
import torch.nn as nn
from torchvision import datasets, transforms
import os
import random
import matplotlib.pyplot as plt
import torch.nn.functional as F
from PIL import Image

# 1. Define Model Structure
class AgriBlock(nn.Module):
    def __init__(self, in_channels, out_channels, expansion=4, stride=1):
        super(AgriBlock, self).__init__()
        self.stride = stride
        hidden_dim = in_channels * expansion
        self.use_res_connect = self.stride == 1 and in_channels == out_channels
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, hidden_dim, 1, 1, 0, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True),
            nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True),
            nn.Conv2d(hidden_dim, out_channels, 1, 1, 0, bias=False),
            nn.BatchNorm2d(out_channels),
        )
    def forward(self, x):
        if self.use_res_connect: return x + self.conv(x)
        else: return self.conv(x)

class AgriNet(nn.Module):
    def __init__(self, num_classes=38):
        super(AgriNet, self).__init__()
        self.stem = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU6(inplace=True)
        )
        self.blocks = nn.Sequential(
            AgriBlock(32, 64, expansion=4, stride=1),
            AgriBlock(64, 128, expansion=6, stride=2),
            AgriBlock(128, 256, expansion=6, stride=2),
            AgriBlock(256, 512, expansion=6, stride=2),
        )
        self.gap = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
    def forward(self, x):
        x = self.stem(x)
        x = self.blocks(x)
        features = self.gap(x)
        x = features.view(features.size(0), -1)
        return self.classifier(x)

# 2. Config
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "agrinet_mixed_v1.pth")
PV_DIR = os.path.join(os.path.dirname(__file__), "plantvillage dataset", "color")
FIELD_DIR = os.path.join(os.path.dirname(__file__), "PlantDoc-Dataset", "test")

def main():
    print(f"Loading Base 38-class Model on {DEVICE}...")
    
    # 3. Get original 38 class names
    pv_dataset = datasets.ImageFolder(PV_DIR)
    class_names = pv_dataset.classes
    
    # 4. Load Pretrained Model
    model = AgriNet(num_classes=38).to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()
    
    # 5. Transforms for prediction
    test_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # 6. Randomly grab some noisy field images from PlantDoc
    field_dataset = datasets.ImageFolder(FIELD_DIR)
    num_samples = 6
    indices = random.sample(range(len(field_dataset)), num_samples)
    
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle('Zero-Shot Domain Transfer: Testing on Wild Field Data (PlantDoc)', fontsize=20, y=0.98)
    
    print("\nPredicting on PlantDoc...")
    for i, idx in enumerate(indices):
        img_path, field_label_idx = field_dataset.imgs[idx]
        field_class_name = field_dataset.classes[field_label_idx]
        
        # Open raw image for plotting
        img_raw = Image.open(img_path).convert("RGB")
        
        # Prepare for model
        input_tensor = test_transforms(img_raw).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            outputs = model(input_tensor)
            probs = F.softmax(outputs, dim=1)
            
            # Get Top 3 Predictions
            top3_prob, top3_idx = torch.topk(probs, 3)
            
        # Plotting
        ax = plt.subplot(2, 3, i + 1)
        ax.imshow(img_raw)
        ax.axis('off')
        
        # Real Label (PlantDoc Name)
        title = f"Ground Truth (PlantDoc):\n{field_class_name}\n\nTop 3 Predictions (38-Class Model):\n"
        
        for k in range(3):
            prob = top3_prob[0][k].item() * 100
            pred_class = class_names[top3_idx[0][k]]
            
            title += f"{k+1}. {pred_class} ({prob:.1f}%)\n"
            
        ax.set_title(title, loc='left', fontsize=10)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    os.makedirs(os.path.join(os.path.dirname(__file__), "evaluation_results"), exist_ok=True)
    out_path = os.path.join(os.path.dirname(__file__), "evaluation_results", "zero_shot_field_test.png")
    plt.savefig(out_path)
    print(f"\nSaved Field Test visualization to: {out_path}")
    plt.show()

if __name__ == "__main__":
    main()
