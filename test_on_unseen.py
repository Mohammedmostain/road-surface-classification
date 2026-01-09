import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import os

# --- CONFIGURATION ---
MODEL_PATH = "road_model.keras"
TEST_PATH = "test_dataset" # <--- Points to the unseen data
IMG_HEIGHT = 180
IMG_WIDTH = 180
BATCH_SIZE = 32

def test_model():
    if not os.path.exists(TEST_PATH):
        print(f"Error: '{TEST_PATH}' not found. Did you run the splitter?")
        return

    print("Loading Model...")
    model = tf.keras.models.load_model(MODEL_PATH)
    
    print(f"Loading Unseen Data from {TEST_PATH}...")
    # Load dataset without shuffling order so we can match labels
    test_ds = tf.keras.utils.image_dataset_from_directory(
        TEST_PATH,
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        shuffle=False 
    )
    
    class_names = test_ds.class_names
    print(f"Classes: {class_names}")

    # Extract Images and Labels
    y_true = []
    y_pred = []
    
    print("Running predictions...")
    for images, labels in test_ds:
        # Predict batch
        preds = model.predict(images, verbose=0)
        pred_classes = np.argmax(preds, axis=1)
        
        y_true.extend(labels.numpy())
        y_pred.extend(pred_classes)

    # --- REPORT ---
    print("\n------------------------------------------------")
    print("FINAL EXAM RESULTS (UNSEEN DATA)")
    print("------------------------------------------------")
    print(classification_report(y_true, y_pred, target_names=class_names))

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', 
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('AI Prediction')
    plt.ylabel('Actual Truth')
    plt.title('Performance on Unseen Data')
    plt.show()

if __name__ == "__main__":
    test_model()