import tensorflow as tf
import numpy as np
import os

# --- CONFIGURATION ---
MODEL_PATH = "road_model.keras"
# Define your classes exactly as they appear in your labeled_dataset folders
# Usually they are alphabetical:
CLASS_NAMES = ['clear_road', 'fully_covered', 'partially_covered'] 

def predict_road_condition(image_path):
    # 1. Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
        return

    print(f"\nAnalyzing: {image_path} ...")

    # 2. Load the trained brain
    # (We load it here, but in a real loop you'd load it once at the top)
    model = tf.keras.models.load_model(MODEL_PATH)

    # 3. Pre-process the image
    # The AI expects a 180x180 pixel square, just like we trained it
    img = tf.keras.utils.load_img(image_path, target_size=(180, 180))
    
    # Convert image to an array of numbers
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch of 1

    # 4. Make the Prediction
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # 5. Interpret Results
    top_class_index = np.argmax(score)
    top_class_name = CLASS_NAMES[top_class_index]
    confidence = 100 * np.max(score)

    print("------------------------------------------------")
    print(f"RESULT: {top_class_name.upper()}")
    print(f"Confidence: {confidence:.2f}%")
    print("------------------------------------------------")
    
    # Print full breakdown for debugging
    print("Detailed breakdown:")
    for i, class_name in enumerate(CLASS_NAMES):
        print(f"  - {class_name}: {100 * score[i]:.2f}%")

if __name__ == "__main__":
    # --- CHANGE THIS TO TEST DIFFERENT IMAGES ---
    test_image = "traffic_screenshots/test_image.png" 
    
    # If that file doesn't exist, let's just pick the first one we find to test
    if not os.path.exists(test_image):
        all_files = os.listdir("traffic_screenshots")
        if all_files:
            test_image = os.path.join("traffic_screenshots", all_files[0])
    
    predict_road_condition(test_image)