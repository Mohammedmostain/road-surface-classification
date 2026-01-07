import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import os

# --- CONFIGURATION ---
MODEL_PATH = "road_model.keras"
DATASET_PATH = "labeled_dataset"
IMG_HEIGHT = 180
IMG_WIDTH = 180
BATCH_SIZE = 32

def evaluate():
    if not os.path.exists(MODEL_PATH):
        print("Error: Model not found. Run train_model.py first.")
        return

    print("Loading Model and Data...")
    
    # 1. Load the Trained Brain
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # 2. Re-load the SAME Validation data used during training
    # (We use seed=123 to ensure we get the exact same split of images)
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_PATH,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        shuffle=False # IMPORTANT: Don't shuffle so predictions match labels
    )
    
    class_names = val_ds.class_names
    print(f"Classes: {class_names}")

    # 3. Get Predictions
    print("\nRunning predictions on validation set...")
    predictions = model.predict(val_ds)
    predicted_classes = np.argmax(predictions, axis=1)
    
    # 4. Get True Labels
    true_labels = np.concatenate([y for x, y in val_ds], axis=0)

    # --- REPORT 1: The Metrics ---
    print("\n------------------------------------------------")
    print("CLASSIFICATION REPORT")
    print("------------------------------------------------")
    print(classification_report(true_labels, predicted_classes, target_names=class_names))

    # --- REPORT 2: The Confusion Matrix (Heatmap) ---
    cm = confusion_matrix(true_labels, predicted_classes)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.ylabel('Actual Truth')
    plt.xlabel('AI Prediction')
    plt.title('Confusion Matrix (Where did it mess up?)')
    plt.show()

if __name__ == "__main__":
    evaluate()