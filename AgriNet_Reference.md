# AgriNet: Custom CNN Reference Implementation (PyTorch)

This document provides the blueprint for building and training your custom model for the AgriVision 2.0 Major Project.

## 1. Custom CNN Architecture: AgriNet

This architecture uses **Inverted Residual Blocks** and **Depthwise Separable Convolutions** to be computationally efficient while satisfying the "from scratch" requirement.

```python
import torch
import torch.nn as nn

class AgriBlock(nn.Module):
    """Inverted Residual Block with Squeeze-and-Excitation"""
    def __init__(self, in_channels, out_channels, expansion=4, stride=1):
        super(AgriBlock, self).__init__()
        self.stride = stride
        hidden_dim = in_channels * expansion
        
        self.use_res_connect = self.stride == 1 and in_channels == out_channels

        self.conv = nn.Sequential(
            # 1x1 Expansion
            nn.Conv2d(in_channels, hidden_dim, 1, 1, 0, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True),
            
            # 3x3 Depthwise
            nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True),
            
            # 1x1 Projection (Linear)
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
        
        # Initial Stem
        self.stem = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU6(inplace=True)
        )
        
        # Layers (increasing filters)
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
```

## 2. Advanced Training Strategy

### Data Loading & Augmentation
```python
from torchvision import transforms

train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
```

### Dual-Task Training (Categorization + Severity)
If you want to add severity estimation, modify the `forward` method:
```python
class AgriNetV2(AgriNet):
    def __init__(self, num_classes=38):
        super().__init__(num_classes)
        self.severity_head = nn.Linear(512, 1) # Regressor for 0-100%

    def forward(self, x):
        # ... feature extraction ...
        disease = self.classifier(features)
        severity = torch.sigmoid(self.severity_head(features))
        return disease, severity
```

## 3. Dataset Links (Free & Easy)
- **PlantVillage (Base)**: [Kaggle Link](https://www.kaggle.com/datasets/abdallahalansary/plant-village-dataset)
- **PlantDoc (Field Images)**: [GitHub Link](https://github.com/pratikkayal/PlantDoc-Dataset)
- **Plant Pathology 2021**: [Kaggle Competition Dataset](https://www.kaggle.com/c/plant-pathology-2021-fgvc8)

## 4. Next Steps for Implementation
1.  **Environment**: Set up PyTorch with CUDA support.
2.  **Preprocessing**: Combine datasets into a unified directory structure.
3.  **Training**: Start with a small learning rate (1e-4) and use `EarlyStopping`.
4.  **Hardware**: Use Google Colab (Free GPU) if local hardware is limited.
