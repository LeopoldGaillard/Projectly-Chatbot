import streamlit as st
import requests
import json
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage

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
        return json.loads(response.content)
    else:
        return {"error": "Unable to fetch data"}
    
def generate_answer_not_really_good(llm, prompt, rag_info):
    
    if rag_info != []:
        prompt = f"Q: {prompt}. Based on my research: {rag_info} A: "

    output = llm(
            prompt, # Prompt
            max_tokens=80, # Maximum number of tokens to generate
            stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
        )

    response = output['choices'][0]['text']

    return response


def generate_good_answer(llm, prompt):
    rag_context = rag_search(prompt)
    
    system_message = """You are a professional in finance.
        As a financial expert, you're here to assist customers with information and advice on various financial topics.
        Example:
        
        Input:
        What are the best investment options for long-term growth?
        
        Context:
        The best investment options for long-term growth include:
        1. Diversified Stock Market Portfolios
        2. Real Estate Investment
        3. Exchange-Traded Funds (ETFs)
        
        Output:
        For long-term growth, consider diversifying your investments with a mix of stocks, real estate, and ETFs.
        """
    

    # rajouter un if rag_context != [] pour le cas ou il n'y a pas de réponse et mettre un message sans le contexte
    if rag_context != []:
        template = f"""Input:
            {prompt}
            
            Context:
            {rag_context}
            
            Output:
            """
    else:
        template = f"""Input:
            {prompt}
            
            Output:
            """
    output = llm(
            template, # Prompt
        )

    response = output['choices'][0]['text']

    return response

#def generate2(llm, prompt):