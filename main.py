# Inspo Chatbot for Public: Can not storage chat history

import os
from dotenv import dotenv_values
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# Configure Streamlit on head
st.set_page_config(
    page_title="AI Productivity Assistant",
    page_icon="https://img.icons8.com/?size=100&id=3fxG1r3aX8Qo&format=png&color=000000",
    layout="centered"
)
# Page title
st.image("https://i.gifer.com/LMkz.gif", use_column_width="always")
st.title("Hello!")
st.write("Today is a good day to work!")
st.caption("Inspo AI Chatbot | Model: meta-llama/Llama-3.1-70B")

# Function resolves response thread from Groq
def parse_groq_stream(stream):
    response = ""
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
    return response


try:
    secrets = dotenv_values(".env")  # for dev env
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except:
    secrets = st.secrets  # for streamlit deployment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

# Save the api_key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
INITIAL_MSG = secrets["INITIAL_MSG"]
CHAT_CONTEXT = secrets["CHAT_CONTEXT"]

client = Groq()

# initialize the chat history if present as streamlit session
if "chat_history" not in st.session_state:
    # print("message not in chat session")
    st.session_state.chat_history = [
        {"role": "assistant",
         "content": INITIAL_RESPONSE
         },
    ]

# Modify style
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
# Hide component of Streamlit
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# the messages in chat_history will be stored as {"role":"user/assistant", "content":"msg}
# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar='https://pub-821312cfd07a4061bf7b99c1f23ed29b.r2.dev/v1/dynamic/color/flash-dynamic-color.png'):
        st.markdown(message["content"])

# user input field
user_prompt = st.chat_input("Try: What I need to do?...")

if user_prompt:
    # Display message from user
    with st.chat_message("user", avatar="https://pub-821312cfd07a4061bf7b99c1f23ed29b.r2.dev/v1/dynamic/color/chat-dynamic-color.png"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    # Get a response from the LLM
    messages = [
        {"role": "system", "content": CHAT_CONTEXT},
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    # Display response message of assistant
    with st.chat_message("assistant", avatar='https://pub-821312cfd07a4061bf7b99c1f23ed29b.r2.dev/v1/dynamic/color/flash-dynamic-color.png'):
        stream = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            stream=True  # for streaming the message
        )
        response = st.write(parse_groq_stream(stream))
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})

