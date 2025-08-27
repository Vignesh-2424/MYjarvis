🤖 JARVIS AI Assistant

A Python-based AI assistant inspired by Iron Man’s J.A.R.V.I.S., capable of voice interaction, facial recognition, natural language understanding, media control, and smart automation.

With features like reminders, music playback, NLP responses, and deep learning-based wake word detection, this project brings a personal AI assistant experience to your system.

🚀 Features

🎙️ Voice Recognition – Understands and processes spoken commands

👀 Facial Recognition – Authenticate users with OpenCV

⏰ Reminders & Memory – Save and recall important tasks/events

🎵 Media Control – Play/pause music on Spotify via voice

🧠 NLP Integration – Natural language responses to queries

🔔 Wake Word Detection – Always-on listening with CNN model

🌐 Integration Ready – Extendable with APIs & tools like Ollama

🛠️ Tech Stack

Python (Core AI logic)

OpenCV (Facial recognition)

SpeechRecognition (Voice input)

Deep Learning (CNN, Keras, TensorFlow) (Wake word detection)

Ollama (LLM-powered responses)

📂 Project Structure
MYJARVIS/
│── dataset/  
│   └── audio/  
│   └── voice_activation_dataset.csv  
│
│── modelling/  
│   ├── cnn_label_encoder.pkl  
│   ├── cnn_wake_model.h5  
│
│── modules/  
│   ├── memory.py  
│   ├── nlp_response.py  
│   ├── spotify_control.py  
│   ├── voice_input.py  
│
│── preprocessing/  
│   ├── cnn_features.npy  
│   ├── cnn_label_encoder.pkl  
│   ├── cnn_labels.npy  
│   ├── preprocess.py  
│
│── gui.py              # Assistant GUI  
│── main.py             # Main entry point  
│── predict.py          # Run predictions  
│── train_cnn_model.py  # Model training script  
│── enroll_voicy.py     # User voice enrollment  
│── memory.json         # Stored reminders/memory  
│── requirement.txt     # Dependencies  
│── temp.wav            # Temporary audio file  
│── .env                # Config & API keys  

⚡ Getting Started
1️⃣ Install Requirements
pip install -r requirement.txt

2️⃣ Run the Assistant
python main.py

3️⃣ Train Wake Word Model (optional)
python train_cnn_model.py

🎯 Future Enhancements

Smart home IoT integration

Advanced conversational AI with Ollama LLMs

Multilingual support

Mobile companion app
