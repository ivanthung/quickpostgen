import streamlit as st
from openai import OpenAI

# Function to convert audio to text using Whisper API
def transcribe_audio(uploaded_file):
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=uploaded_file,
        response_format="text"
    )
    return transcription


# Streamlit App Interface
def run_app():
    st.title("Audio to Text Conversion using OpenAI's Whisper API")

    uploaded_file = st.file_uploader("Upload an audio file. ", type=["mp3", "wav", "ogg", "flac"], )

    if uploaded_file is not None:
        with st.spinner('Processing...'):
            transcription = transcribe_audio(uploaded_file)

            if 'error' in transcription:
                st.error("Error: " + transcription['error'])
            else:
                st.success("Conversion Successful!")
                st.text_area("Text Output", transcription, height=300)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
run_app()
