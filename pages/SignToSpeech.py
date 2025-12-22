import streamlit as st
import numpy as np
import cv2
import tensorflow as tf
import pandas as pd
import time
import tempfile
from gtts import gTTS
from utils.mediapipe_utils import extract_keypoints, movement_energy
import mediapipe as mp

# ===================== LOAD MODEL & LABELS =====================
model = tf.keras.models.load_model("models/signbridge_robust_model.h5", compile=False)

labels_df = pd.read_excel("data/labels.xlsx")
labels_df["SignID"] = labels_df["SignID"].astype(str).str.zfill(4)
labels_df = labels_df[
    (labels_df["SignID"].astype(int) >= 289) &
    (labels_df["SignID"].astype(int) <= 400)
].reset_index(drop=True)

words_ar = labels_df["Sign-Arabic"].values
words_en = labels_df["Sign-English"].values

# ===================== MEDIAPIPE =====================
mp_holistic = mp.solutions.holistic
mp_draw = mp.solutions.drawing_utils

holistic = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ===================== TTS =====================
def generate_tts(text, lang):
    if not text.strip():
        return None
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# ===================== UI =====================
st.title("Sign → Speech")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Camera Feed")
    FRAME_WINDOW = st.image([])

with col2:
    st.subheader("Recognized Word")
    word_display = st.empty()
    state_display = st.empty()

    st.subheader("Phrase")
    phrase_display = st.empty()

    st.subheader("Speech Output")
    speak_en_btn = st.button("Speak English Phrase", use_container_width=True)
    speak_ar_btn = st.button("التحدث باللغة العربية", use_container_width=True)

    en_audio_placeholder = st.empty()
    ar_audio_placeholder = st.empty()

# ===================== SESSION STATE =====================
defaults = {
    "running": False,
    "phrase_list": [],
    "en_audio_path": None,
    "ar_audio_path": None,
    "last_phrase_key_en": "",
    "last_phrase_key_ar": "",
    "speak_en_request": False,
    "speak_ar_request": False,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ===================== CONTROL BUTTONS =====================
start_btn = st.button("Start Video Stream")
stop_btn = st.button("Stop Video Stream")
clear_btn = st.button("Clear Phrase")

if start_btn:
    st.session_state.running = True

if stop_btn:
    st.session_state.running = False

if clear_btn:
    st.session_state.phrase_list = []
    st.session_state.en_audio_path = None
    st.session_state.ar_audio_path = None
    st.session_state.last_phrase_key_en = ""
    st.session_state.last_phrase_key_ar = ""

# ===================== BUTTON FLAGS =====================
if speak_en_btn:
    st.session_state.speak_en_request = True

if speak_ar_btn:
    st.session_state.speak_ar_request = True

# ===================== PARAMETERS =====================
WINDOW_SIZE = 48
START_THRESHOLD = 0.015
PREDICT_COOLDOWN = 2.0

sequence = []
prev_kp = None
last_predict_time = 0
state = "IDLE"
final_ar = "..."
final_en = "..."

# ===================== CAMERA LOOP =====================
camera = cv2.VideoCapture(0)

try:
    while st.session_state.running:
        ret, img = camera.read()
        if not ret:
            st.error("Camera not found")
            break

        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = holistic.process(rgb)
        keypoints = extract_keypoints(results)

        # ---------- STATE MACHINE ----------
        if prev_kp is not None:
            energy = movement_energy(prev_kp, keypoints)
            if energy > START_THRESHOLD and time.time() - last_predict_time > PREDICT_COOLDOWN:
                state = "RECORDING"

        if state == "RECORDING":
            sequence.append(keypoints)
            if len(sequence) == WINDOW_SIZE:
                state = "PREDICT"

        if state == "PREDICT":
            X = np.expand_dims(sequence, axis=0)
            probs = model.predict(X, verbose=0)[0]
            idx = int(np.argmax(probs))

            final_ar = words_ar[idx]
            final_en = words_en[idx]
            st.session_state.phrase_list.append(f"{final_en} ({final_ar})")

            sequence = []
            last_predict_time = time.time()
            state = "COOLDOWN"

        if state == "COOLDOWN" and time.time() - last_predict_time >= PREDICT_COOLDOWN:
            state = "IDLE"

        prev_kp = keypoints

        # ---------- DRAW ----------
        if results.left_hand_landmarks:
            mp_draw.draw_landmarks(img, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        if results.right_hand_landmarks:
            mp_draw.draw_landmarks(img, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # ---------- TEXT ----------
        english_phrase = " ".join(w.split(" (")[0] for w in st.session_state.phrase_list)
        arabic_phrase = " ".join(w.split(" (")[1].rstrip(")") for w in st.session_state.phrase_list)

        word_display.text(f"Arabic: {final_ar}\nEnglish: {final_en}")
        state_display.text(f"State: {state}")
        phrase_display.text(f"English: {english_phrase}\nArabic: {arabic_phrase}")

        FRAME_WINDOW.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    camera.release()
    cv2.destroyAllWindows()

except Exception as e:
    camera.release()
    st.error(e)

# ===================== SPEECH OUTPUT (OUTSIDE LOOP) =====================
english_phrase = " ".join(w.split(" (")[0] for w in st.session_state.phrase_list)
arabic_phrase = " ".join(w.split(" (")[1].rstrip(")") for w in st.session_state.phrase_list)

# ---- ENGLISH ----
if st.session_state.speak_en_request and english_phrase:
    if st.session_state.last_phrase_key_en != english_phrase:
        st.session_state.en_audio_path = generate_tts(english_phrase, "en")
        st.session_state.last_phrase_key_en = english_phrase

    if st.session_state.en_audio_path:
        en_audio_placeholder.audio(st.session_state.en_audio_path, format="audio/mp3")

    st.session_state.speak_en_request = False

# ---- ARABIC ----
if st.session_state.speak_ar_request and arabic_phrase:
    if st.session_state.last_phrase_key_ar != arabic_phrase:
        st.session_state.ar_audio_path = generate_tts(arabic_phrase, "ar")
        st.session_state.last_phrase_key_ar = arabic_phrase

    if st.session_state.ar_audio_path:
        ar_audio_placeholder.audio(st.session_state.ar_audio_path, format="audio/mp3")

    st.session_state.speak_ar_request = False

# ===================== Floating bottom-right converter button =====================
st.markdown(
    """
    <style>
    .switch-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        left: auto !important;
        z-index: 9999;
    }
    .switch-button button {
        background-color: #0d7a7a;
        color: white;
        border-radius: 25px;
        padding: 0.6em 1.4em;
        font-weight: 600;
        font-family: 'Nunito', sans-serif;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
    }
    .switch-button button:hover {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="switch-button">', unsafe_allow_html=True)

if st.button("Switch to Speech → Sign", key="switch_to_speech_to_sign"):
    st.session_state.mode = "speech_to_sign"
    st.switch_page("pages/SpeechToSign.py")  # Update path if needed

st.markdown('</div>', unsafe_allow_html=True)
