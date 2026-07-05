# FarmLens ML Model - Training & Testing Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Dataset](#dataset)
3. [Model Architecture](#model-architecture)
4. [Training Process](#training-process)
5. [Testing & Evaluation](#testing--evaluation)
6. [Results](#results)
7. [Usage](#usage)
8. [How to Reproduce](#how-to-reproduce)

---

## 1. Overview

FarmLens uses a **MobileNetV2-based deep learning model** for plant disease detection. The model is trained on the PlantVillage dataset and can classify images into 38 different categories (14 crops × various diseases + healthy states).

### Key Features:
- **Architecture**: MobileNetV2 (Transfer Learning)
- **Framework**: PyTorch
- **Input**: 224×224 RGB images
- **Output**: 38 disease classes
- **Accuracy**: 85-95% (depending on class)
- **Inference Time**: ~50-100ms per image (CPU)

---

## 2. Dataset

### PlantVillage Dataset
- **Source**: Kaggle - PlantVillage Dataset
- **Total Images**: ~54,000 images
- **Image Size**: Variable (resized to 224×224)
- **Format**: JPEG/PNG
- **Classes**: 38 categories

### Dataset Structure:
```
dataset/
├── train/           # Training set (~70%)
│   ├── Apple___Apple_scab/
│   ├── Apple___Black_rot/
│   ├── Apple___Cedar_apple_rust/
│   ├── Apple___healthy/
│   ├── Corn_(maize)___Common_rust_/
│   ├── Potato___Early_blight/
│   ├── Tomato___Late_blight/
│   └── ... (38 classes total)
├── valid/           # Validation set (~15%)
│   └── ... (same structure)
└── test/            # Test set (~15%)
    └── ... (same structure)
```

### Supported Crops (14):
1. Apple
2. Blueberry
3. Cherry
4. Corn (Maize)
5. Grape
6. Orange
7. Peach
8. Pepper (Bell)
9. Potato
10. Raspberry
11. Soybean
12. Squash
13. Strawberry
14. Tomato

### Disease Categories (38 total):
- Fungal diseases (rust, blight, mildew, mold, scab, rot)
- Bacterial diseases (bacterial spot)
- Viral diseases (mosaic virus, leaf curl virus)
- Pest damage (spider mites)
- Healthy plants

---

## 3. Model Architecture

### Base Model: MobileNetV2
- **Pre-trained on**: ImageNet (1.4M images, 1000 classes)
- **Architecture**: Inverted residual blocks with linear bottlenecks
- **Parameters**: ~3.5 million
- **Advantages**:
  - Lightweight (9.3 MB)
  - Fast inference
  - Good accuracy
  - Mobile-friendly

### Transfer Learning Approach:
```python
# 1. Load pre-trained MobileNetV2
model = models.mobilenet_v2(pretrained=True)

# 2. Freeze early layers (feature extraction)
for param in model.features.parameters():
    param.requires_grad = False

# 3. Replace classifier for 38 classes
model.classifier[1] = nn.Sequential(
    nn.Dropout(0.2),
    nn.Linear(1280, 38)  # 38 output classes
)
```

### Model Layers:
```
Input (224×224×3)
    ↓
MobileNetV2 Features (frozen)
    ↓
Global Average Pooling
    ↓
Dropout (0.2)
    ↓
Fully Connected (1280 → 38)
    ↓
Softmax
    ↓
Output (38 classes)
```

---

## 4. Training Process

### Hyperparameters:
```python
{
    'num_epochs': 25,
    'batch_size': 32,
    'learning_rate': 0.001,
    'optimizer': 'Adam',
    'loss_function': 'CrossEntropyLoss',
    'scheduler': 'StepLR (step_size=7, gamma=0.1)',
    'device': 'CUDA (if available) / CPU'
}
```

### Data Augmentation (Training):
- Random horizontal flip
- Random rotation (±10°)
- Color jitter (brightness, contrast, saturation ±20%)
- Resize to 224×224
- Normalization (ImageNet stats)

### Training Pipeline:

#### Step 1: Data Preparation
```bash
# Load and augment training data
# Load validation data (no augmentation)
# Create data loaders
```

#### Step 2: Model Initialization
```bash
# Load pre-trained MobileNetV2
# Freeze feature extraction layers
# Replace classifier
# Move to GPU/CPU
```

#### Step 3: Training Loop
```bash
For each epoch:
    # Training phase
    - Forward pass
    - Calculate loss
    - Backward pass
    - Update weights
    
    # Validation phase
    - Evaluate on validation set
    - Track metrics
    - Save best model
    
    # Learning rate scheduling
    - Reduce LR every 7 epochs
```

#### Step 4: Model Saving
```bash
# Save best model weights
# Save class names
# Generate training plots
```

### Training Time:
- **GPU (NVIDIA RTX 3080)**: ~2-3 hours
- **CPU (Intel i7)**: ~8-12 hours

---

## 5. Testing & Evaluation

### Test Metrics:

#### 1. Overall Metrics:
- **Accuracy**: Overall classification accuracy
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall

#### 2. Per-Class Metrics:
- Individual accuracy for each of 38 classes
- Confusion matrix
- Support (number of test samples per class)

#### 3. Performance Metrics:
- Inference time per image
- Throughput (images/second)
- Model size

### Evaluation Process:

```bash
# 1. Load trained model
model = load_model('mobilenetv2_plant.pth')

# 2. Load test data
test_loader = prepare_test_data()

# 3. Run inference
predictions, labels = test_model(model, test_loader)

# 4. Calculate metrics
accuracy, precision, recall, f1 = calculate_metrics()

# 5. Generate visualizations
- Confusion matrix
- Per-class performance charts
- ROC curves (optional)
```

### Visualization Outputs:
1. **confusion_matrix.png** - Shows prediction accuracy across all classes
2. **per_class_metrics.png** - Bar charts for precision, recall, F1, support
3. **test_results.json** - Detailed metrics in JSON format

---

## 6. Results

### Expected Performance:

#### Overall Metrics:
```
Accuracy:  85-95%
Precision: 83-93%
Recall:    82-92%
F1-Score:  83-92%
```

#### Best Performing Classes (F1 > 0.95):
- Apple___healthy
- Blueberry___healthy
- Corn_(maize)___healthy
- Potato___healthy
- Tomato___healthy

#### Challenging Classes (F1 < 0.80):
- Corn_(maize)___Cercospora_leaf_spot
- Grape___Leaf_blight
- Tomato___Spider_mites

#### Inference Performance:
```
Device: CPU (Intel i7)
- Average time: 50-100ms per image
- Throughput: 10-20 images/sec

Device: GPU (NVIDIA RTX 3080)
- Average time: 10-20ms per image
- Throughput: 50-100 images/sec
```

---

## 7. Usage

### Using the Trained Model:

#### In Python:
```python
import torch
from torchvision import transforms, models
from PIL import Image
import json

# Load model
model = models.mobilenet_v2(pretrained=False)
model.classifier[1] = nn.Sequential(
    nn.Dropout(0.2),
    nn.Linear(1280, 38)
)
model.load_state_dict(torch.load('mobilenetv2_plant.pth'))
model.eval()

# Load class names
with open('class_names.json', 'r') as f:
    class_names = json.load(f)

# Preprocess image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

img = Image.open('plant_image.jpg')
img_tensor = transform(img).unsqueeze(0)

# Predict
with torch.no_grad():
    output = model(img_tensor)
    probs = torch.softmax(output, dim=1)
    confidence, predicted = torch.max(probs, 1)

# Get result
disease = class_names[predicted.item()]
confidence = confidence.item()

print(f"Prediction: {disease}")
print(f"Confidence: {confidence:.2%}")
```

#### In FarmLens API:
The model is automatically used as a fallback when Gemini API is unavailable:
```
User uploads image
    ↓
Try Gemini API (primary)
    ↓ (if fails)
Use PyTorch Model (fallback) ← This model
    ↓
Return prediction
```

---

## 8. How to Reproduce

### Prerequisites:
```bash
# Python 3.8+
# PyTorch 1.10+
# torchvision
# scikit-learn
# matplotlib
# seaborn
# Pillow
```

### Step 1: Install Dependencies
```bash
cd backend
pip install torch torchvision scikit-learn matplotlib seaborn pillow
```

### Step 2: Prepare Dataset
```bash
# Download PlantVillage dataset from Kaggle
# Extract to backend/dataset/
# Structure should be:
#   dataset/train/
#   dataset/valid/
#   dataset/test/
```

### Step 3: Train Model
```bash
python train_model.py
```

**Output:**
- `mobilenetv2_plant.pth` - Trained model weights
- `class_names.json` - List of 38 classes
- `training_history.png` - Training/validation curves

**Expected Training Time:**
- GPU: 2-3 hours
- CPU: 8-12 hours

### Step 4: Test Model
```bash
python test_model.py
```

**Output:**
- `confusion_matrix.png` - Confusion matrix visualization
- `per_class_metrics.png` - Per-class performance charts
- `test_results.json` - Detailed metrics

### Step 5: Use in FarmLens
The trained model is automatically integrated into the FarmLens backend and will be used as a fallback when Gemini API is unavailable.

---

## 📊 Sample Results

### Training Curves:
![Training History](training_history.png)
*Loss and accuracy curves showing model convergence*

### Confusion Matrix:
![Confusion Matrix](confusion_matrix.png)
*Normalized confusion matrix showing per-class accuracy*

### Per-Class Metrics:
![Per-Class Metrics](per_class_metrics.png)
*Precision, recall, F1-score, and support for each class*

---

## 🔧 Troubleshooting

### Common Issues:

#### 1. Out of Memory (OOM)
**Solution**: Reduce batch size in CONFIG
```python
'batch_size': 16  # or 8
```

#### 2. Slow Training
**Solution**: Use GPU or reduce epochs
```python
'num_epochs': 10  # instead of 25
```

#### 3. Low Accuracy
**Solutions**:
- Train for more epochs
- Increase data augmentation
- Unfreeze more layers
- Use a larger model

#### 4. Model Not Loading
**Solution**: Check PyTorch version compatibility
```bash
pip install torch==1.13.0 torchvision==0.14.0
```

---

## 📚 References

1. **PlantVillage Dataset**: https://www.kaggle.com/datasets/emmarex/plantdisease
2. **MobileNetV2 Paper**: https://arxiv.org/abs/1801.04381
3. **PyTorch Documentation**: https://pytorch.org/docs/
4. **Transfer Learning Guide**: https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

---

## 👥 Contributors

- FarmLens Team
- Dataset: PlantVillage Project
- Model Architecture: Google Research (MobileNetV2)

---

## 📄 License

This model is trained on the PlantVillage dataset which is publicly available for research purposes.

---

**Last Updated**: April 2026  
**Version**: 1.0.0
