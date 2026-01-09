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
    # 1. Check if model exists
    if not os.path.exists(MODEL_PATH):
        print("Error: Model not found. Did you remember to run 'train_model.py' after cleaning?")
        return

    print("Loading Model and Data...")
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # 2. Load the Validation Split (20% of data)
    # We MUST shuffle to ensure we get a random mix of Clear, Full, and Partial
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_PATH,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        shuffle=True 
    )
    
    class_names = val_ds.class_names
    print(f"Classes found: {class_names}")

    # 3. Extract Images and Labels
    # We iterate through the dataset to separate images from their true labels
    print("Running predictions on clean validation data...")
    all_images = []
    all_labels = []

    for images, labels in val_ds:
        all_images.append(images.numpy())
        all_labels.append(labels.numpy())

    x_test = np.concatenate(all_images)
    y_true = np.concatenate(all_labels)

    # 4. Predict
    predictions = model.predict(x_test, verbose=0)
    y_pred = np.argmax(predictions, axis=1)

    # --- REPORT 1: The Numbers ---
    print("\n------------------------------------------------")
    print("CLASSIFICATION REPORT")
    print("------------------------------------------------")
    print(classification_report(y_true, y_pred, target_names=class_names))

    # --- REPORT 2: The Heatmap ---
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.ylabel('Actual Truth')
    plt.xlabel('AI Prediction')
    plt.title('Confusion Matrix (Clean Data)')
    plt.show()

if __name__ == "__main__":
    evaluate()