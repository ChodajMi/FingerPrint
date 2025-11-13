import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Data generators
train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

training_set = train_datagen.flow_from_directory(r"dataset/train_set",
                                                 target_size=(64, 64),
                                                 batch_size=32,
                                                 class_mode='categorical')

test_datagen = ImageDataGenerator(rescale=1./255)

test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size=(64, 64),
                                            batch_size=32,
                                            class_mode='categorical')

# Build CNN model for 10 classes
cnn = tf.keras.models.Sequential()
cnn.add(tf.keras.layers.Conv2D(input_shape=[64, 64, 3], filters=32, kernel_size=3, activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
cnn.add(tf.keras.layers.Flatten())
cnn.add(tf.keras.layers.Dense(units=128, activation='relu'))
cnn.add(tf.keras.layers.Dense(units=10, activation='softmax'))  # 10 classes

cnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
cnn.fit(training_set, validation_data=test_set, epochs=10)

# Save the model
cnn.save('my_model_updated.keras')

print("Model retrained and saved as my_model_updated.keras")

# Test loading
try:
    loaded_model = tf.keras.models.load_model('my_model_updated.keras')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
