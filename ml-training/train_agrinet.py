import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from tqdm import tqdm

# ==========================================
# 1. Custom CNN Architecture: AgriNet
# ==========================================
class AgriBlock(nn.Module):
    """Inverted Residual Block"""
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
        if self.use_res_connect:
            return x + self.conv(x)
        else:
            return self.conv(x)

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
        x = self.gap(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


# ==========================================
# 2. Training Setup & Hyperparameters
# ==========================================
# Path to the dataset you just added
DATA_DIR = os.path.join(os.path.dirname(__file__), "plantvillage dataset", "color")

# Hyperparameters
BATCH_SIZE = 16      # Reduced for GTX 1650 (4GB VRAM)
NUM_EPOCHS = 10
LEARNING_RATE = 0.001
VAL_SPLIT = 0.2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_dataloaders():
    # Transforms (Data Augmentation for Training, standard normalization for Validation)
    train_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Load dataset using ImageFolder (it automatically reads the 38 class folders)
    print(f"Loading dataset from: {DATA_DIR}")
    dataset = datasets.ImageFolder(root=DATA_DIR)
    
    # Split into train and validation
    val_size = int(len(dataset) * VAL_SPLIT)
    train_size = len(dataset) - val_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    
    # Apply specific transforms to the splits
    train_dataset.dataset.transform = train_transforms
    
    # Copy dataset to avoid overriding train transforms, apply val transforms
    import copy
    val_dataset_transformed = copy.deepcopy(val_dataset)
    val_dataset_transformed.dataset.transform = val_transforms

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True)
    val_loader = DataLoader(val_dataset_transformed, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True)
    
    return train_loader, val_loader, dataset.classes


# ==========================================
# 3. Main Training Loop
# ==========================================
def train_model():
    print(f"Using device: {device}")
    
    train_loader, val_loader, class_names = get_dataloaders()
    print(f"Found {len(class_names)} classes.")
    print(f"Training samples: {len(train_loader.dataset)} | Validation samples: {len(val_loader.dataset)}")
    
    model = AgriNet(num_classes=len(class_names)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2, verbose=True)

    best_val_loss = float('inf')
    os.makedirs(os.path.join(os.path.dirname(__file__), "models"), exist_ok=True)
    save_path = os.path.join(os.path.dirname(__file__), "models", "agrinet_v1.pth")

    for epoch in range(NUM_EPOCHS):
        print(f"\nEpoch {epoch+1}/{NUM_EPOCHS}")
        print("-" * 20)
        
        # --- Training Phase ---
        model.train()
        running_loss = 0.0
        running_corrects = 0
        
        # tqdm for progress bar
        train_bar = tqdm(train_loader, desc="Training")
        for inputs, labels in train_bar:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            
            train_bar.set_postfix(loss=loss.item())

        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = running_corrects.double() / len(train_loader.dataset)
        print(f"Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

        # --- Validation Phase ---
        model.eval()
        val_loss = 0.0
        val_corrects = 0
        
        with torch.no_grad():
            val_bar = tqdm(val_loader, desc="Validation")
            for inputs, labels in val_bar:
                inputs, labels = inputs.to(device), labels.to(device)
                
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                _, preds = torch.max(outputs, 1)
                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(preds == labels.data)

        epoch_val_loss = val_loss / len(val_loader.dataset)
        epoch_val_acc = val_corrects.double() / len(val_loader.dataset)
        print(f"Val Loss: {epoch_val_loss:.4f} Acc: {epoch_val_acc:.4f}")
        
        # Adjust learning rate based on validation loss
        scheduler.step(epoch_val_loss)

        # Save Best Model
        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            torch.save(model.state_dict(), save_path)
            print(f"==> Model saved to {save_path} (improved val_loss)")

    print(f"\nTraining Complete. Best validation loss: {best_val_loss:.4f}")
    print(f"Model saved at: {save_path}")

if __name__ == '__main__':
    train_model()
