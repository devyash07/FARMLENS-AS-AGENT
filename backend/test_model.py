"""
Plant Disease Detection Model Testing Script
============================================

This script tests the trained MobileNetV2 model and generates
comprehensive evaluation metrics and visualizations.

Author: FarmLens Team
Date: 2026
"""

import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score,
    precision_recall_fscore_support
)
from pathlib import Path
import time

# Configuration
CONFIG = {
    'model_path': 'mobilenetv2_plant.pth',
    'class_names_path': 'class_names.json',
    'test_data_dir': './dataset/test',  # or './dataset/valid'
    'batch_size': 32,
    'device': 'cuda' if torch.cuda.is_available() else 'cpu',
    'image_size': 224,
}

print("=" * 70)
print("FARMLENS - MODEL TESTING & EVALUATION")
print("=" * 70)
print(f"\nConfiguration:")
print(f"  Device: {CONFIG['device']}")
print(f"  Model: {CONFIG['model_path']}")
print(f"  Test Data: {CONFIG['test_data_dir']}")
print("=" * 70)


def load_model_and_classes():
    """
    Load the trained model and class names
    """
    print("\n[1/5] Loading Model...")
    
    # Load class names
    with open(CONFIG['class_names_path'], 'r') as f:
        class_names = json.load(f)
    
    num_classes = len(class_names)
    
    # Build model architecture
    model = models.mobilenet_v2(pretrained=False)
    model.classifier[1] = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(model.classifier[1].in_features, num_classes)
    )
    
    # Load trained weights
    model.load_state_dict(torch.load(CONFIG['model_path'], map_location=CONFIG['device']))
    model = model.to(CONFIG['device'])
    model.eval()
    
    print(f"  ✓ Model loaded successfully")
    print(f"  ✓ Number of classes: {num_classes}")
    print(f"  ✓ Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    return model, class_names


def prepare_test_data():
    """
    Prepare test data loader
    """
    print("\n[2/5] Preparing Test Data...")
    
    test_transforms = transforms.Compose([
        transforms.Resize((CONFIG['image_size'], CONFIG['image_size'])),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    test_dataset = datasets.ImageFolder(
        root=CONFIG['test_data_dir'],
        transform=test_transforms
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=CONFIG['batch_size'],
        shuffle=False,
        num_workers=4
    )
    
    print(f"  ✓ Test samples: {len(test_dataset)}")
    print(f"  ✓ Batch size: {CONFIG['batch_size']}")
    
    return test_loader


def test_model(model, test_loader):
    """
    Test the model and collect predictions
    """
    print("\n[3/5] Testing Model...")
    
    all_preds = []
    all_labels = []
    all_probs = []
    
    start_time = time.time()
    
    with torch.no_grad():
        for batch_idx, (inputs, labels) in enumerate(test_loader):
            inputs = inputs.to(CONFIG['device'])
            labels = labels.to(CONFIG['device'])
            
            outputs = model(inputs)
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
            
            if (batch_idx + 1) % 10 == 0:
                print(f"  Processed {(batch_idx + 1) * CONFIG['batch_size']} samples...")
    
    inference_time = time.time() - start_time
    avg_time_per_image = inference_time / len(all_preds)
    
    print(f"\n  ✓ Testing complete!")
    print(f"  ✓ Total time: {inference_time:.2f}s")
    print(f"  ✓ Average time per image: {avg_time_per_image*1000:.2f}ms")
    print(f"  ✓ Throughput: {len(all_preds)/inference_time:.2f} images/sec")
    
    return np.array(all_preds), np.array(all_labels), np.array(all_probs)


def generate_metrics(preds, labels, class_names):
    """
    Generate comprehensive evaluation metrics
    """
    print("\n[4/5] Generating Metrics...")
    
    # Overall accuracy
    accuracy = accuracy_score(labels, preds)
    print(f"\n  Overall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Per-class metrics
    precision, recall, f1, support = precision_recall_fscore_support(
        labels, preds, average=None, zero_division=0
    )
    
    # Classification report
    print("\n  Detailed Classification Report:")
    print("  " + "=" * 66)
    report = classification_report(labels, preds, target_names=class_names, zero_division=0)
    print("  " + report.replace("\n", "\n  "))
    
    # Top 5 best performing classes
    print("\n  Top 5 Best Performing Classes:")
    print("  " + "-" * 66)
    f1_with_names = list(zip(class_names, f1, support))
    f1_with_names.sort(key=lambda x: x[1], reverse=True)
    for i, (name, f1_score, supp) in enumerate(f1_with_names[:5], 1):
        print(f"  {i}. {name:40s} F1: {f1_score:.4f} (n={int(supp)})")
    
    # Top 5 worst performing classes
    print("\n  Top 5 Worst Performing Classes:")
    print("  " + "-" * 66)
    for i, (name, f1_score, supp) in enumerate(f1_with_names[-5:], 1):
        print(f"  {i}. {name:40s} F1: {f1_score:.4f} (n={int(supp)})")
    
    return accuracy, precision, recall, f1, support


def plot_confusion_matrix(preds, labels, class_names):
    """
    Plot confusion matrix
    """
    print("\n[5/5] Generating Visualizations...")
    
    # Compute confusion matrix
    cm = confusion_matrix(labels, preds)
    
    # Normalize confusion matrix
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    # Plot
    plt.figure(figsize=(20, 18))
    sns.heatmap(
        cm_normalized,
        annot=True,
        fmt='.2f',
        cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names,
        cbar_kws={'label': 'Accuracy'}
    )
    plt.title('Confusion Matrix (Normalized)', fontsize=16, pad=20)
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    
    print(f"  ✓ Confusion matrix saved to: confusion_matrix.png")


def plot_per_class_metrics(class_names, precision, recall, f1, support):
    """
    Plot per-class performance metrics
    """
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    x = np.arange(len(class_names))
    
    # Precision
    axes[0, 0].bar(x, precision, color='skyblue')
    axes[0, 0].set_title('Precision per Class', fontsize=14)
    axes[0, 0].set_ylabel('Precision')
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(class_names, rotation=90, ha='right')
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Recall
    axes[0, 1].bar(x, recall, color='lightcoral')
    axes[0, 1].set_title('Recall per Class', fontsize=14)
    axes[0, 1].set_ylabel('Recall')
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(class_names, rotation=90, ha='right')
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # F1-Score
    axes[1, 0].bar(x, f1, color='lightgreen')
    axes[1, 0].set_title('F1-Score per Class', fontsize=14)
    axes[1, 0].set_ylabel('F1-Score')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(class_names, rotation=90, ha='right')
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Support (number of samples)
    axes[1, 1].bar(x, support, color='plum')
    axes[1, 1].set_title('Number of Test Samples per Class', fontsize=14)
    axes[1, 1].set_ylabel('Count')
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(class_names, rotation=90, ha='right')
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('per_class_metrics.png', dpi=300, bbox_inches='tight')
    
    print(f"  ✓ Per-class metrics saved to: per_class_metrics.png")


def save_results(accuracy, precision, recall, f1, support, class_names):
    """
    Save results to JSON file
    """
    results = {
        'overall_accuracy': float(accuracy),
        'per_class_metrics': []
    }
    
    for i, class_name in enumerate(class_names):
        results['per_class_metrics'].append({
            'class': class_name,
            'precision': float(precision[i]),
            'recall': float(recall[i]),
            'f1_score': float(f1[i]),
            'support': int(support[i])
        })
    
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"  ✓ Results saved to: test_results.json")


def main():
    """
    Main testing pipeline
    """
    try:
        # Step 1: Load model
        model, class_names = load_model_and_classes()
        
        # Step 2: Prepare test data
        test_loader = prepare_test_data()
        
        # Step 3: Test model
        preds, labels, probs = test_model(model, test_loader)
        
        # Step 4: Generate metrics
        accuracy, precision, recall, f1, support = generate_metrics(preds, labels, class_names)
        
        # Step 5: Generate visualizations
        plot_confusion_matrix(preds, labels, class_names)
        plot_per_class_metrics(class_names, precision, recall, f1, support)
        save_results(accuracy, precision, recall, f1, support, class_names)
        
        print("\n" + "=" * 70)
        print("TESTING COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"\nGenerated Files:")
        print(f"  • confusion_matrix.png - Confusion matrix visualization")
        print(f"  • per_class_metrics.png - Per-class performance metrics")
        print(f"  • test_results.json - Detailed results in JSON format")
        print(f"\nOverall Model Accuracy: {accuracy*100:.2f}%")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
