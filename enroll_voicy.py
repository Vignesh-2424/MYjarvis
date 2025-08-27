from resemblyzer import VoiceEncoder, preprocess_wav
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os

# Path to save your voice sample and embedding
AUDIO_PATH = "data/your_voice.wav"
EMBEDDING_PATH = "data/your_embedding.npy"

def record_voice(seconds=3, fs=16000):
    print(f"🎙️ Recording for {seconds} seconds. Please say 'Hey Jarvis' clearly...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("✅ Recording complete.")
    return fs, recording

def save_wav(file_path, fs, recording):
    wav.write(file_path, fs, recording)

def generate_and_save_embedding(audio_path, embedding_path):
    encoder = VoiceEncoder()
    wav_data = preprocess_wav(audio_path)
    embedding = encoder.embed_utterance(wav_data)
    np.save(embedding_path, embedding)
    print("✅ Voice embedding saved.")

def main():
    os.makedirs("data", exist_ok=True)
    fs, rec = record_voice()
    save_wav(AUDIO_PATH, fs, rec)
    generate_and_save_embedding(AUDIO_PATH, EMBEDDING_PATH)

if __name__ == "__main__":
    main()
