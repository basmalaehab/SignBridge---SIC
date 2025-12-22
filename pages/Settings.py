import streamlit as st

st.title("Settings")
st.write("Adjust your app preferences here.")

# Initialize global text size in session state
if "text_size" not in st.session_state:
    st.session_state.text_size = 16  # default 16px

# Slider to change text size
text_size = st.slider("Set text size for all pages", min_value=12, max_value=24, value=st.session_state.text_size)
st.session_state.text_size = text_size

st.write(f"Current text size: {st.session_state.text_size}px")

# Apply text size via CSS
st.markdown(
    f"""
    <style>
    body, h1, h2, h3, h4, h5, h6, p, div, span {{
        font-size: {st.session_state.text_size}px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
