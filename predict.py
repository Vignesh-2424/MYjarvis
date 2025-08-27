import librosa
import numpy as np
import pickle
import speech_recognition as sr
from tensorflow.keras.models import load_model
from modules.nlp_response import get_response

# Load model and label encoder
model = load_model("modelling/jarvis_voice_model.h5")
with open("modelling/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Function to extract MFCC
def extract_mfcc(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    return mfcc_mean

# Record voice
def listen_and_predict():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("🎤 Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Save temporary wav
        with open("temp.wav", "wb") as f:
            f.write(audio.get_wav_data())

        mfcc = extract_mfcc("temp.wav")
        mfcc = mfcc.reshape(1, -1)
        prediction = model.predict(mfcc)
        predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])[0]

        print(f"🗣️ You said (predicted): {predicted_label}")
        response = get_response(predicted_label)
        print("🤖 Jarvis:", response)

    except Exception as e:
        print("❌ Error:", e)

# Run loop
while True:
    listen_and_predict()
    print("\nSay 'exit' to stop or press Ctrl+C")
