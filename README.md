# FinSync AI

Implementation of a chatbot using Llama2.

We use the library streamlit to display the chatbot in a web page.

The chatbot can do RAG searches (with low performance at the moment).

## Llama model

The used model can be uploaded here :
https://huggingface.co/TheBloke/Llama-2-7B-GGUF/tree/main

Be free to use another model by changing the value of the 'MODEL_PATH' variable in the chatbot.py file.

## Launch the chatbot

You need to launch the <a href="https://github.com/LeopoldGaillard/Projectly-api-rag" target="_blank">RAG API</a>
before launching the chatbot so that it can make requests.

Execute the run.sh script to launch the chatbot and you will find it on :

http://172.24.56.153:8501/
