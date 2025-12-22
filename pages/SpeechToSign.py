import streamlit as st

# Initialize mode
if "mode" not in st.session_state:
    st.session_state.mode = "speech_to_sign"

st.title("Speech → Sign")
st.caption("Convert spoken words into sign language")

# Divide page into 2 equal columns
col1, col2 = st.columns(2)

# LEFT column: microphone / text input
with col1:
    st.subheader("Text Input / Microphone")
    audio_value = st.audio_input("Record high quality audio", sample_rate=48000)

    if audio_value:
        st.audio(audio_value)

# RIGHT column: animated avatar
with col2:
    st.subheader("Sign Avatar")
    st.write("Animated sign language avatar will appear here")

# Floating bottom-right switch button
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

if st.button("Switch to Sign → Speech", key="switch_to_sign_to_speech"):
    st.session_state.mode = "sign_to_speech"
    st.switch_page("pages/SignToSpeech.py")

st.markdown('</div>', unsafe_allow_html=True)
