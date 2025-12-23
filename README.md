# SignBridge: Real-Time Sign Language Translator


SignBridge is a Python-based Streamlit application that enables real-time translation between sign language and spoken language. The platform currently supports Sign → Speech translation and includes a Speech → Sign avatar system (planned). The system is designed to improve accessibility and communication for deaf and hard-of-hearing individuals, while providing a scalable solution for enterprise integration, including potential smart-device OEM deployment.

---

## Table of Contents

1. [Features](#features)  
2. [Demo](#demo)  
3. [Installation](#installation)  
4. [Project Structure](#project-structure)  
5. [How to Use](#how-to-use)  
6. [Dependencies](#dependencies)  
7. [Future Work](#future-work)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## Features

- Sign → Speech Translation: Converts real-time sign gestures into text and spoken language.  
- Speech → Sign (Avatar): Converts spoken words into animated sign language (avatar placeholder).  
- Dual-language Support: English and Arabic.  
- Phrase Library: Stores commonly used phrases to speed up repeated communication.  
- User-Friendly Interface: Simple Streamlit UI with camera input, text display, and audio output.  
- Scalable Architecture: Mobile-ready and potentially integratable into smart devices (OEM).  

---

## Demo

### Sign → Speech


- Shows camera feed with recognized signs  
- Displays recognized words and phrases in English and Arabic  
- Converts phrases to speech using gTTS  

### Speech → Sign


- Users can input speech via microphone  
- Placeholder for animated sign avatar  

---

## Installation

1. Clone the repository

Bash

git clone https://github.com/basmalaehab/SignBridge.git
cd SignBridge

2. Create and activate virtual environment
   
Bash

   python -m venv sign_env
    # Windows
    sign_env\Scripts\activate
    # Linux/Mac
    source sign_env/bin/activate
    

3. Install requirements
    
Bash

    pip install -r requirements.txt

    

4. Run the application
  
Bash

   streamlit run SignBridge.py

  

Project Structure
Bash

SignBridge/
├── SignBridge.py
├── pages/
│   ├── SignToSpeech.py
│   ├── SpeechToSign.py
│   ├── Learn.py
│   ├── Library.py
│   └── Settings.py
├── models/
│   └── signbridge_robust_model.h5
├── data/
│   └── labels.xlsx
├── utils/
│   └── mediapipe_utils.py
├── requirements.txt
└── README.md

  
---

## How to Use

### Sign → Speech

- Open the app and select Sign → Speech.
- Click Start Video Stream to begin capturing gestures.
- Recognized words appear in English and Arabic.
- Click Speak English Phrase or التحدث باللغة العربية to hear the output.
- Clear Phrase button resets the session.

### Speech → Sign
- Switch to Speech → Sign page.
- Record audio or type text.
- Animated sign avatar will display the translation (future implementation).

### Navigation

- Use the top navigation menu to switch between Translate, Explore, and Preferences.
- Floating buttons allow quick switching between Sign → Speech and Speech → Sign modes.

---

## Dependencies
- Python 3.10+
- Streamlit
- TensorFlow
- OpenCV
- Mediapipe
- gTTS
- NumPy, Pandas
- Other dependencies in requirements.txt


---

## Future Work
- Full Speech → Sign avatar implementation
- Mobile deployment
- Enterprise/OEM integration (smart TVs, streaming platforms)
- Multi-language expansion beyond English & Arabic
- Enhanced phrase prediction and adaptive library
