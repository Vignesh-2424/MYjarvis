import os
import numpy as np
import pandas as pd
import librosa
import librosa.display
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import pickle

CSV_PATH = "../dataset/voice_activation_dataset.csv"
AUDIO_DIR = "../dataset/audio"
OUTPUT_FEATURES = "cnn_features.npy"
OUTPUT_LABELS = "cnn_labels.npy"
ENCODER_PATH = "cnn_label_encoder.pkl"

# Load dataset
df = pd.read_csv(CSV_PATH)
print(f"🔍 Loaded {len(df)} entries")

# Extract Mel-spectrograms
X = []
y = []
labels = []

for index, row in df.iterrows():
    filename = row['filename']
    label = row['label']
    path = os.path.join(AUDIO_DIR, filename)

    try:
        y_audio, sr = librosa.load(path, sr=16000)
        mel_spec = librosa.feature.melspectrogram(y=y_audio, sr=sr, n_mels=40)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        # Resize to a fixed shape (40 x 100 frames)
        if mel_spec_db.shape[1] < 100:
            pad_width = 100 - mel_spec_db.shape[1]
            mel_spec_db = np.pad(mel_spec_db, ((0,0),(0,pad_width)), mode='constant')
        else:
            mel_spec_db = mel_spec_db[:, :100]

        X.append(mel_spec_db)
        y.append(label)
        if label not in labels:
            labels.append(label)

        print(f"[✓] Processed {filename}")

    except Exception as e:
        print(f"[✘] Failed {filename}: {e}")

# Encode labels
label_to_index = {l: i for i, l in enumerate(sorted(labels))}
index_to_label = {i: l for l, i in label_to_index.items()}
y_encoded = [label_to_index[label] for label in y]

# Save encoder
with open(ENCODER_PATH, "wb") as f:
    pickle.dump(index_to_label, f)

# Convert to arrays
X = np.array(X)
y_encoded = np.array(y_encoded)
X = X[..., np.newaxis]  # Add channel dimension for CNN

# Save features
np.save(OUTPUT_FEATURES, X)
np.save(OUTPUT_LABELS, y_encoded)

print("\n✅ Preprocessing complete.")
print(f"🎯 X shape: {X.shape}")
print(f"🎯 y shape: {y_encoded.shape}")
