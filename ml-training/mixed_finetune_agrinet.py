import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, ConcatDataset, Dataset
from torchvision import datasets, transforms
import os
from tqdm import tqdm
from PIL import Image

# ==========================================
# 1. AGRINET ARCHITECTURE
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
# 2. CONFIGURATION & DATA MAPPING
# ==========================================
BASE_DIR = os.path.dirname(__file__)
PV_DIR = os.path.join(BASE_DIR, "plantvillage dataset", "color")
PD_TRAIN_DIR = os.path.join(BASE_DIR, "PlantDoc-Dataset", "train")
PRETRAINED_MODEL = os.path.join(BASE_DIR, "models", "agrinet_v1.pth")
SAVE_MODEL = os.path.join(BASE_DIR, "models", "agrinet_mixed_v1.pth")

BATCH_SIZE = 16
NUM_EPOCHS = 10
LEARNING_RATE = 0.0001 # 10x smaller because we are fine-tuning an already perfect model!
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Manual Mapping: PlantDoc folder names -> exact PlantVillage folder names
PLANTDOC_TO_PV_MAP = {
    "Apple Scab Leaf": "Apple___Apple_scab",
    "Apple leaf": "Apple___healthy",
    "Apple rust leaf": "Apple___Cedar_apple_rust",
    "Bell_pepper leaf": "Pepper,_bell___healthy",
    "Bell_pepper leaf spot": "Pepper,_bell___Bacterial_spot",
    "Blueberry leaf": "Blueberry___healthy",
    "Cherry leaf": "Cherry_(including_sour)___healthy",
    "Corn Gray leaf spot": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn leaf blight": "Corn_(maize)___Northern_Leaf_Blight",
    "Corn rust leaf": "Corn_(maize)___Common_rust_",
    "Peach leaf": "Peach___healthy",
    "Potato leaf early blight": "Potato___Early_blight",
    "Potato leaf late blight": "Potato___Late_blight",
    "Raspberry leaf": "Raspberry___healthy",
    "Soyabean leaf": "Soybean___healthy",
    "Squash Powdery mildew leaf": "Squash___Powdery_mildew",
    "Strawberry leaf": "Strawberry___healthy",
    "Tomato Early blight leaf": "Tomato___Early_blight",
    "Tomato Septoria leaf spot": "Tomato___Septoria_leaf_spot",
    "Tomato leaf": "Tomato___healthy",
    "Tomato leaf bacterial spot": "Tomato___Bacterial_spot",
    "Tomato leaf late blight": "Tomato___Late_blight",
    "Tomato leaf mosaic virus": "Tomato___Tomato_mosaic_virus",
    "Tomato leaf yellow virus": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "grape leaf": "Grape___healthy",
    "grape leaf black rot": "Grape___Black_rot"
    # Note: any PlantDoc class not in this map will be ignored to keep 38 classes clean.
}

# Custom Dataset Wrapper to map labels
class MappedPlantDocDataset(Dataset):
    def __init__(self, root_dir, pv_class_to_idx, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.pv_class_to_idx = pv_class_to_idx
        self.samples = []
        
        # Build samples
        for folder_name in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder_name)
            if not os.path.isdir(folder_path): continue
                
            # If we don't know how to map this PlantDoc class, skip it
            if folder_name not in PLANTDOC_TO_PV_MAP:
                print(f"Skipping unknown PlantDoc class: {folder_name}")
                continue
                
            pv_target_name = PLANTDOC_TO_PV_MAP[folder_name]
            target_idx = pv_class_to_idx[pv_target_name]
            
            for img_name in os.listdir(folder_path):
                img_path = os.path.join(folder_path, img_name)
                self.samples.append((img_path, target_idx))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, target = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, target


# ==========================================
# 3. TRAINING LOGIC
# ==========================================
def main():
    print(f"Starting MIXED DOMAIN Fine-Tuning on {device}")
    
    # 1. Base Augmentations
    transforms_pipeline = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # 2. Get PlantVillage base mapping (to ensure 38 classes are correct order)
    pv_dataset = datasets.ImageFolder(PV_DIR, transform=transforms_pipeline)
    pv_class_to_idx = pv_dataset.class_to_idx
    
    # 3. Map PlantDoc
    pd_dataset = MappedPlantDocDataset(PD_TRAIN_DIR, pv_class_to_idx, transform=transforms_pipeline)
    print(f"Loaded {len(pv_dataset)} PlantVillage base images.")
    print(f"Loaded {len(pd_dataset)} PlantDoc mapped field images.")
    
    # 4. Combine Datasets!
    mixed_dataset = ConcatDataset([pv_dataset, pd_dataset])
    
    # Split into Train/Val (80/20)
    val_size = int(0.2 * len(mixed_dataset))
    train_size = len(mixed_dataset) - val_size
    train_data, val_data = torch.utils.data.random_split(mixed_dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True)
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True)

    # 5. Load Model (Keep 38 heads)
    model = AgriNet(num_classes=38).to(device)
    print(f"Loading Base Weights: {PRETRAINED_MODEL}")
    model.load_state_dict(torch.load(PRETRAINED_MODEL, map_location=device))
    
    # We fine-tune the WHOLE model, but with a tiny learning rate in Adam,
    # so we don't destroy the knowledge it already has.
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
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
                
        epoch_loss = running_loss / len(train_data)
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
                    
        val_epoch_loss = val_loss / len(val_data)
        val_epoch_acc = val_correct / val_total
        print(f"Val Loss: {val_epoch_loss:.4f} Acc: {val_epoch_acc:.4f}")
        
        # Save Best Model
        if val_epoch_loss < best_val_loss:
            best_val_loss = val_epoch_loss
            print(f"==> Mixed Domain Adaptation successful. Saved robust model to {SAVE_MODEL}")
            torch.save(model.state_dict(), SAVE_MODEL)

if __name__ == "__main__":
    main()
