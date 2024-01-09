from langchain.chat_models import ChatOpenAI
from StreamHandler import StreamHandler
from langchain.schema import HumanMessage, SystemMessage
from functions import *
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

st.set_page_config(page_title="FinSync AI", page_icon="💸")

st.title("Boost your business ! 🚀")
st.sidebar.title('FinSync AI 🤖💸')

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

prompt = st.chat_input("Your message")

if prompt:
    
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    chat_box = st.empty()
    stream_handler = StreamHandler(chat_box, display_method='write')
    chat = ChatOpenAI(api_key=OPEN_AI_KEY, streaming=True, callbacks=[stream_handler])

    rag_context = rag_search(prompt)

    messages = [
        SystemMessage(
            content=f"""You are a professional in finance.
             As a financial expert, you're here to assist customers with information and advice on various financial topics.
             {rag_context}"""
        ),
        HumanMessage(content=prompt),
    ]
    st.chat_message("assistant").markdown(messages[0])
    response = chat(messages)
    
    llm_response = response.content
    st.session_state.messages.append({'role': 'assistant', 'content': llm_response})