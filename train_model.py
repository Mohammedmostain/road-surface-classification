import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import os

# --- CONFIGURATION ---
DATASET_PATH = "labeled_dataset"
IMG_HEIGHT = 180
IMG_WIDTH = 180
BATCH_SIZE = 32
EPOCHS = 15  # How many times the AI studies the entire dataset

def train_brain():
    print("------------------------------------------------")
    print("Phase 1: Loading Data")
    print("------------------------------------------------")
    
    # 1. Load Training Data (80% of images)
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_PATH,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE
    )

    # 2. Load Validation Data (20% of images - used for testing)
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_PATH,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE
    )

    class_names = train_ds.class_names
    print(f"\nClasses found: {class_names}")
    
    # optimize performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    print("\n------------------------------------------------")
    print("Phase 2: Building the CNN Architecture")
    print("------------------------------------------------")

    model = models.Sequential([
        # Layer 1: Rescaling (Make pixels numbers between 0 and 1)
        layers.Rescaling(1./255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        
        # Layer 2: Convolution (The "Eyes") - Finds edges and simple shapes
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(), # Reduces size (focuses on important parts)

        # Layer 3: Convolution (The "Cortex") - Finds textures (snow vs asphalt)
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),

        # Layer 4: Convolution (The "Deep Vision") - Finds complex patterns
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        
        # Layer 5: Flatten (Turn the 2D image into a long list of numbers)
        layers.Flatten(),
        
        # Layer 6: Dense (The "Brain") - Makes the final decision
        layers.Dense(128, activation='relu'),
        
        # Layer 7: Output - One score for each class (Clear, Full, Partial)
        layers.Dense(len(class_names))
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.summary()

    print("\n------------------------------------------------")
    print("Phase 3: Training (The Learning Process)")
    print("------------------------------------------------")
    
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS
    )

    print("\n------------------------------------------------")
    print("Phase 4: Saving the Brain")
    print("------------------------------------------------")
    
    model.save('road_model.keras')
    print("SUCCESS! Model saved to 'road_model.keras'")
    
    # Optional: Show a graph of how well it learned
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    plt.plot(acc, label='Training Accuracy')
    plt.plot(val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training Results')
    plt.show()

if __name__ == "__main__":
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Folder '{DATASET_PATH}' not found. Run manual_sorter.py first!")
    else:
        train_brain()