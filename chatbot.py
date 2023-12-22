from llama_cpp import Llama
from functions import *

MODEL_PATH = "models/llama-2-7b.Q8_0.gguf"

llm = Llama(model_path=MODEL_PATH, max_tokens=100, n_ctx=2048)

#warmup(llm)

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
    with st.spinner("Thinking...") :

        response = generate_answer(llm, prompt)

        st.chat_message("assistant").markdown(response)

        st.session_state.messages.append({'role': 'assistant', 'content': response})