import streamlit as st

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you today?"}]


def warmup(llm):
    i = 0
    while (i != 2):
        output = llm(
            "Hello",
            max_tokens=32,
        )
        i += 1

def generate_answer(llm, prompt):

    output = llm(
            "Q: "+ prompt +" A: ", # Prompt
            max_tokens=80, # Maximum number of tokens to generate
            stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
        )

    response = output['choices'][0]['text']

    return response