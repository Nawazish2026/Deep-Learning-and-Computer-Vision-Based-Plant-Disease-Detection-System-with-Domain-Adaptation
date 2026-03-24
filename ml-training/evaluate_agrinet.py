import torch
import torch.nn as nn
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from tqdm import tqdm

# Import AgriNet from the training script logic
# (Or redefine it here if the scripts are separate)
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
        x = self.classifier(x)
        return x

# ==============================
# CONFIGURATION
# ==============================
DATA_DIR = os.path.join(os.path.dirname(__file__), "plantvillage dataset", "color")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "agrinet_mixed_v1.pth")
BATCH_SIZE = 32
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def evaluate():
    print(f"Starting Evaluation on: {device}")
    
    # 1. Load Data
    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    full_dataset = datasets.ImageFolder(root=DATA_DIR, transform=val_transforms)
    class_names = full_dataset.classes
    
    # Use 20% validation split same as training
    val_size = int(0.2 * len(full_dataset))
    train_size = len(full_dataset) - val_size
    _, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size], generator=torch.Generator().manual_seed(42))
    
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

    # 2. Load Model
    model = AgriNet(num_classes=len(class_names)).to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()
    
    all_preds = []
    all_labels = []

    # 3. Predict
    print("Running inference on validation set...")
    with torch.no_grad():
        for inputs, labels in tqdm(val_loader):
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    # 4. Generate Classification Report
    print("\n" + "="*50)
    print("CLASSIFICATION REPORT")
    print("="*50)
    print(classification_report(all_labels, all_preds, target_names=class_names))

    # 5. Confusion Matrix
    print("Generating Confusion Matrix...")
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(20, 15))
    sns.heatmap(cm, annot=False, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('AgriNet-V1 Confusion Matrix')
    
    os.makedirs(os.path.join(os.path.dirname(__file__), "evaluation_results"), exist_ok=True)
    report_path = os.path.join(os.path.dirname(__file__), "evaluation_results", "confusion_matrix.png")
    plt.savefig(report_path)
    print(f"Confusion Matrix saved to: {report_path}")
    
    plt.show()

if __name__ == "__main__":
    evaluate()
