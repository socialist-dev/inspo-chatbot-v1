# Inspo Chatbot for Public: Can not storage chat history

import os
from dotenv import dotenv_values
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# Function resolves response thread from Groq
def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


# streamlit page configuration
st.set_page_config(
    page_title="INSPO - AI Productivity Assistant",
    page_icon="https://i.gifer.com/LMkz.gif",
    layout="centered"
)

# Style with CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    secrets = dotenv_values(".env")  # for dev env
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except:
    secrets = st.secrets  # for streamlit deployment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

# save the api_key to environment variable
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

# Hide components of Streamlit
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Page title
st.image("https://i.gifer.com/LMkz.gif", use_column_width="always")
st.title("Hello!")
st.write("Today is a good day to work!")
st.caption("Inspo AI Chatbot | Model: meta-llama/Llama-3.1-70B")
# the messages in chat_history will be stored as {"role":"user/assistant", "content":"msg}
# display chat history
for message in st.session_state.chat_history:
    # print("message in chat session")
    with st.chat_message("role", avatar='https://pub-821312cfd07a4061bf7b99c1f23ed29b.r2.dev/v1/dynamic/color/flash-dynamic-color.png'):
        st.markdown(message["content"])


# user input field
user_prompt = st.chat_input("Try: What I need to do?...")

if user_prompt:
    # st.chat_message("user").markdown
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    # get a response from the LLM
    messages = [
        {"role": "system", "content": CHAT_CONTEXT
         },
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar='https://pub-821312cfd07a4061bf7b99c1f23ed29b.r2.dev/v1/dynamic/color/flash-dynamic-color.png'):
        stream = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            stream=True  # for streaming the message
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})

