import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import os
import copy
from tqdm import tqdm

# ==========================================
# 1. DEFINE AGRINET (Must match original)
# ==========================================
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

# ==========================================
# 2. CONFIGURATION & DATASETS
# ==========================================
TRAIN_DIR = os.path.join(os.path.dirname(__file__), "PlantDoc-Dataset", "train")
TEST_DIR = os.path.join(os.path.dirname(__file__), "PlantDoc-Dataset", "test")
PRETRAINED_MODEL = os.path.join(os.path.dirname(__file__), "models", "agrinet_v1.pth")
SAVE_MODEL = os.path.join(os.path.dirname(__file__), "models", "agrinet_plantdoc.pth")

BATCH_SIZE = 16 # Keep 16 for GTX 1650
NUM_EPOCHS = 10
LEARNING_RATE = 0.001
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_finetune_data():
    # Advanced augmentations for field data
    train_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    train_dataset = datasets.ImageFolder(root=TRAIN_DIR, transform=train_transforms)
    val_dataset = datasets.ImageFolder(root=TEST_DIR, transform=val_transforms)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True)
    
    return train_loader, val_loader, train_dataset.classes

# ==========================================
# 3. TRANSFER LEARNING LOGIC
# ==========================================
def run_transfer_learning():
    print(f"Starting Domain Adaptation on {device}")
    
    # 1. Load Data
    train_loader, val_loader, classes = get_finetune_data()
    num_new_classes = len(classes)
    print(f"Loaded PlantDoc Dataset. Found {num_new_classes} classes.")
    
    # 2. Load Base Model (Trained on 38 PlantVillage classes)
    model = AgriNet(num_classes=38).to(device)
    print(f"Loading base weights from: {PRETRAINED_MODEL}")
    model.load_state_dict(torch.load(PRETRAINED_MODEL, map_location=device))
    
    # 3. FREEZE THE BASE LAYERS (Feature Extractor)
    for param in model.parameters():
        param.requires_grad = False
        
    print("Pre-trained layers frozen.")
        
    # 4. REPLACE THE CLASSIFIER HEAD
    # The new layer will automatically have requires_grad=True
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(512, num_new_classes)
    ).to(device)
    print(f"Classifier head replaced for {num_new_classes} classes.")
    
    # 5. Define Loss and Optimizer (Only optimize the new classifier!)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=LEARNING_RATE)
    
    # 6. Training Loop (Fast because only the last layer is training)
    best_val_loss = float('inf')
    
    for epoch in range(NUM_EPOCHS):
        print(f"\nEpoch {epoch+1}/{NUM_EPOCHS}")
        print("-" * 20)
        
        # Training
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        with tqdm(train_loader, desc="Training") as pbar:
            for inputs, labels in pbar:
                inputs, labels = inputs.to(device), labels.to(device)
                
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                
                running_loss += loss.item() * inputs.size(0)
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
                
                pbar.set_postfix({'loss': loss.item()})
                
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = correct / total
        print(f"Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")
        
        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            with tqdm(val_loader, desc="Validation") as pbar:
                for inputs, labels in pbar:
                    inputs, labels = inputs.to(device), labels.to(device)
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    
                    val_loss += loss.item() * inputs.size(0)
                    _, predicted = outputs.max(1)
                    val_total += labels.size(0)
                    val_correct += predicted.eq(labels).sum().item()
                    
        val_epoch_loss = val_loss / len(val_loader.dataset)
        val_epoch_acc = val_correct / val_total
        print(f"Val Loss: {val_epoch_loss:.4f} Acc: {val_epoch_acc:.4f}")
        
        # Save Best Model
        if val_epoch_loss < best_val_loss:
            best_val_loss = val_epoch_loss
            print(f"==> Domain Adaptation successful. Saving new head to {SAVE_MODEL}")
            torch.save(model.state_dict(), SAVE_MODEL)

if __name__ == "__main__":
    run_transfer_learning()
