import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import pickle

# Load data
X = np.load("preprocessing/cnn_features.npy")
y = np.load("preprocessing/cnn_labels.npy")

# One-hot encode labels
num_classes = len(set(y))
y = to_categorical(y, num_classes)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Build CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(40, 100, 1)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    
    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Callbacks
checkpoint = ModelCheckpoint("modelling/cnn_wake_model.h5", save_best_only=True, monitor="val_accuracy", mode="max")
early_stop = EarlyStopping(patience=10, restore_best_weights=True)

# Train
model.fit(X_train, y_train,
          validation_data=(X_test, y_test),
          epochs=50,
          batch_size=8,
          callbacks=[checkpoint, early_stop])

# Save encoder (already saved, but for safety)
with open("modelling/cnn_label_encoder.pkl", "wb") as f:
    pickle.dump({0: 'negative', 1: 'postive'}, f)

print("✅ Model trained and saved to modelling/cnn_wake_model.h5")
