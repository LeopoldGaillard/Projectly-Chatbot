import streamlit as st
import requests
import torch
import transformers
import json
from transformers import AutoTokenizer
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA



def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you today?"}]
    
def warmup(llm):
    i = 0
    while (i != 2):
        output = llm(
            "Hello",
            max_tokens=50,
        )
        i += 1

def rag_search(query):

    url = f"http://127.0.0.1:5000/projectly/docs/rag_search/{query}"
    response = requests.get(url)
    if response.status_code == 200:
        res = json.loads(response.content)
        res = {item["_id"]: item["_source"] for item in res}
        return res
    else:
        return {"error": "Unable to fetch data"}
    
def process_context(context_data):

    processed_context = ""
    for key, data in context_data.items():
        context_piece = f"Title: {data['title']}\nDescription: {data['description']}\nContent: {data['content']}\n\n"
        processed_context += context_piece

    return processed_context

def generate_answer(llm, query):
    rag_context = rag_search(query)
    processed_context = process_context(rag_context)


    prompt = f"""You are a professional in finance.
        As a financial expert, you're here to assist customers with information and advice on various financial topics.

        Input: {query}
        Context: {processed_context}
        Output:
        """
    
    output = llm(prompt)

    response = output['choices'][0]['text']

    return response


def generate3(llm, query):

    #tokenizer = AutoTokenizer.from_pretrained(llm)

    query_pipeline = transformers.pipeline(
        "text-generation",
        model=llm,
        device_map="auto",)
    
    llm = HuggingFacePipeline(pipeline=query_pipeline)

    rag_context = rag_search(query)

    template = """You are a professional in finance.
        As a financial expert, you're here to assist customers with information and advice on various financial topics.
        If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise.

        Input: {question}
        Context: {context}
        Output:
        """
    
    #prompt = ChatPromptTemplate.from_template(template)

    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                  chain_type="stuff",
                                  retriever=rag_context,
                                  return_source_documents=True)

    return qa_chain.run(query)
    #return rag_chain.invoke(query)

#def generate2(llm, prompt):