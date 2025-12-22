import streamlit as st

st.set_page_config(
    page_title="SignBridge",
    layout="wide"
)

# Define your pages
pages = {
    "Translate": [
        st.Page("pages/SignToSpeech.py", title="Sign → Speech"),
        st.Page("pages/SpeechToSign.py", title="Speech → Sign"),
    ],
    "Explore": [
        st.Page("pages/Learn.py", title="Tutorials"),
        st.Page("pages/Library.py", title="Try It Out"),
    ],
    "Preferences": [
        st.Page("pages/Settings.py", title="Settings"),
    ],
}

# Navigation menu at the top
pg = st.navigation(pages, position="top")
pg.run()
