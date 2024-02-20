import streamlit as st
from openai import OpenAI
import toml 

# Load your API key (same as before)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
session = st.session_state
default_instructions = "Create a post that we can use for LinkedIn for communications purposes."

if 'ai_report_text' not in session:
    session['ai_report_text'] = ''

def generate_post_stream(instruction, example, background, word_count, engine, container):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    prompt = f"""Background content: {background} 
                  Example post for another project: {example}
                  Instructions: {instruction}
                  Please write a social media post with a word count limit of approximately {word_count} words."""
    
    st.session_state.messages = ({"role": "assistant", "content": prompt})
    
    stream = client.chat.completions.create(
        model=engine,
        messages=[st.session_state.messages],
        stream=True,
    )
    
    text_chunks = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            with container:
                text_chunks.append(chunk.choices[0].delta.content)            
                st.write(''.join(text_chunks))
    session['ai_report_text'] = ''.join(text_chunks)  # Store the text

    
    return stream


# --- Streamlit UI (Modified) ---
st.title("Ivan's Social Media Post Generator")
st.text("This is about 2 cent per generation. Please don't bankrupt me :D")

col1, col2 = st.columns(2)

with col1:
    instruction = st.text_area("Write your instructions for the post", value= default_instructions, height=100)
    example = st.text_area("Provide an example post", height=100)
    word_count = st.text_input("Word count limit:",value=100)
    background = st.text_area("Background content", height=150)

    if "post" not in st.session_state:
        st.session_state.post = ""


with col2:
    engine_choice = st.selectbox("Select GPT-3 Engine", ["gpt-4-0125-preview", "gpt-3.5-turbo-0125"]) 

    container = st.empty()
    if st.button("Generate Post"):
        s = generate_post_stream(instruction, example, background, word_count, engine_choice, container)
        

# --- End of App ---
