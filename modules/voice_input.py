import speech_recognition as sr
import librosa
import numpy as np
import pickle
import os
from tensorflow.keras.models import load_model

# Load CNN model and label encoder
MODEL_PATH = "modelling/cnn_wake_model.h5"
ENCODER_PATH = "modelling/cnn_label_encoder.pkl"

model = load_model(MODEL_PATH)

# Load label encoder (as dictionary)
with open(ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)

# Reverse dictionary lookup: get label name from predicted class (0 or 1)
def get_label_name(index):
    return label_encoder.get(index, "unknown")

# Wake word detection
def predict_wake_word():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Save the audio temporarily
        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())

        # Extract MFCCs
        y, sr_rate = librosa.load("temp.wav", sr=16000)
        mfcc = librosa.feature.mfcc(y=y, sr=sr_rate, n_mfcc=40)

        # Pad or trim to 100 frames
        if mfcc.shape[1] < 100:
            pad_width = 100 - mfcc.shape[1]
            mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
        else:
            mfcc = mfcc[:, :100]

        mfcc = mfcc.reshape(40, 100, 1)  # CNN input shape
        features = np.expand_dims(mfcc, axis=0)

        # Predict
        prediction = model.predict(features)
        predicted_index = np.argmax(prediction, axis=1)[0]
        predicted_label = get_label_name(predicted_index)

        print(f"Predicted: {predicted_label}")
        return predicted_label

    except Exception as e:
        print(f"Error in prediction: {e}")
        return None

# Regular command listening
def listen_to_user():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text

    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError:
        print("API unavailable. Check internet.")
        return None
