import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# --- Configuration ---
# Root directory containing the 'train' and 'test' folders
ROOT_DATA_DIR = r"C:\Users\97517\Desktop\ML_miniproject\Fingerprint_Split_Dataset"

# Define the paths for the training and testing data
TRAIN_DIR = os.path.join(ROOT_DATA_DIR, 'train')
TEST_DIR = os.path.join(ROOT_DATA_DIR, 'test')

# Model Input Parameters
IMAGE_SIZE = (96, 96)  # Common size for fingerprint images; adjust based on your original resolution
BATCH_SIZE = 32        # Number of samples per gradient update
# Since you have 1200 people, this is a 1200-class classification problem
NUM_CLASSES = 1200     
# ---------------------

print("--- Step 1: Defining Data Augmentation and Preprocessing ---")

# 1. Initialize the Data Generator for Training (Includes Augmentation)
# Augmentation helps prevent overfitting by introducing variations in the training data.
# Note: Fingerprints are delicate; use minor transformations.
train_datagen = ImageDataGenerator(
    rescale=1./255,          # Normalize pixel values to 0-1
    rotation_range=5,        # Randomly rotate images by up to 5 degrees
    width_shift_range=0.05,  # Randomly shift images horizontally
    height_shift_range=0.05, # Randomly shift images vertically
    zoom_range=0.05,         # Randomly zoom in on images
    shear_range=0.05,        # Randomly apply shearing transformations
    horizontal_flip=False,   # Fingerprints should not be flipped horizontally
    fill_mode='nearest'      # Strategy for filling in new pixels created by transformations
)

# 2. Initialize the Data Generator for Testing (Only Preprocessing)
# Validation/Test data must NOT be augmented, only normalized/rescaled.
test_datagen = ImageDataGenerator(
    rescale=1./255           # Only normalize pixel values to 0-1
)

print("--- Step 2: Creating Data Flow Generators ---")

# 3. Create the Training Data Generator (Flows from directory)
# This generator automatically labels images based on their subdirectory name (Person ID)
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMAGE_SIZE,
    color_mode='grayscale',     # Fingerprints are typically processed in grayscale
    batch_size=BATCH_SIZE,
    class_mode='categorical',   # Use 'categorical' for 1200 classes
    shuffle=True                # Shuffle training data
)

# 4. Create the Testing Data Generator
test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMAGE_SIZE,
    color_mode='grayscale',
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False               # Do NOT shuffle test data for consistent evaluation
)

print("-" * 50)
print(f"Total batches for Training: {len(train_generator)}")
print(f"Total batches for Testing: {len(test_generator)}")
print("Data generators are ready to be used in model.fit()")

# --- How to Access Information ---
# You can verify the class indices (Person ID to numerical label mapping)
# print("Class Indices Mapping (Person ID -> Label):", train_generator.class_indices)
# print("Image Shape for Model Input:", train_generator.image_shape)

# Example of how to use the generators (The actual training code would go here):
# model = tf.keras.Sequential([...])
# model.compile(...)
# history = model.fit(
#     train_generator,
#     steps_per_epoch=train_generator.samples // BATCH_SIZE, # Use all training samples once per epoch
#     epochs=10,
#     validation_data=test_generator,
#     validation_steps=test_generator.samples // BATCH_SIZE
# )

# NOTE: The final lines showing model usage are commented out as they are part of the next step (model building/training).