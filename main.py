import os
import streamlit as st
from workflow import app,config
from langchain_core.messages import HumanMessage

st.title("🧙‍♂️Journey AI Game")

openai_api_key = os.getenv('OPENAI_API_KEY')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def generate_response(query):
    # add users message in history
    st.session_state.chat_history.append(HumanMessage(query))

    # send whole history to llm
    response = app.invoke({"messages": st.session_state.chat_history}, config)

    # AI last answer
    ai_message = response['messages'][-1]

    # adding him to history return message content
    st.session_state.chat_history.append(ai_message)
    return ai_message.content


# display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# react to user input
if prompt := st.chat_input("Старт"):
    # display user message in chat message container
    st.chat_message("user").markdown(f'{prompt}')
    # add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Assistant: {generate_response(prompt)}"
    # display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})