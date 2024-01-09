import streamlit as st
import requests
import json

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you today?"}]
    
def warmup(llm):
    i = 0
    while (i != 2):
        llm(
            "Hello",
            max_tokens=50,
        )
        i += 1

def rag_search(query):

    url = f"http://127.0.0.1:5000/projectly/docs/rag_search/{query}"
    response = requests.get(url)

    if response.status_code == 200:
        highlighted_texts = []

        for hit in response.json():
            highlight = hit.get('highlight', {})
            text_parts = []

            # Concaténer les highlights de 'title', 'description' et 'content'
            for field in ['title', 'description', 'content']:
                if field in highlight:
                    # Joindre tous les fragments du highlight pour un champ donné
                    text_parts.append(' '.join(highlight[field]))

            # Joindre tous les champs highlightés pour ce document
            highlighted_texts.append(' '.join(text_parts))

        # Joindre les highlights de tous les documents
        all_highlights = ' '.join(highlighted_texts)
        return f"""Potentially relevant context : {all_highlights[:7800]}""" if all_highlights else ""
    else:
        return {"error": "Unable to fetch data"}
    
def process_context(context_data):

    processed_context = ""
    for key, data in context_data.items():
        context_piece = f"Title: {data['title']}\nDescription: {data['description']}\nContent: {data['content']}\n\n"
        processed_context += context_piece

    return f"""Contexte : {processed_context}""" if processed_context else ""

def generate_answer(llm, query):
    rag_context = rag_search(query)
    processed_context = process_context(rag_context)

    prompt = f"""You are a professional in finance.
    As a financial expert, you're here to assist customers with information and advice on various financial topics.
    
    Input: {query}

    {f"Context: {processed_context}" if processed_context else ""}
    
    Output:
    """
    output = llm(prompt)

    response = output['choices'][0]['text']

    return response

def call_chatgpt(oai_key, prompt):
    rag_context = rag_search(prompt)
    processed_context = process_context(rag_context)
    retrieval = processed_context if processed_context else ""

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {oai_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",  # Utilisation du modèle gpt-3.5-turbo
        "messages": [
            {"role": "system",
            "content": f"""You are a professional in finance.
             As a financial expert, you're here to assist customers with information and advice on various financial topics.
             {retrieval}"""
            },
            {"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def extract_text_from_response(prompt):
    response = call_chatgpt(prompt)
    try:
        choices = response.get('choices', [])
        if choices and 'message' in choices[0] and 'content' in choices[0]['message']:
            return choices[0]['message']['content']
        else:
            return "No Answer"
    except Exception as e:
        return "Error in extracting text: " + str(e)
   
def test_streaming(client, prompt):
    
    rag_context = rag_search(prompt)
    processed_context = process_context(rag_context)
    retrieval = processed_context if processed_context else ""

    rep = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
            "content": f"""You are a professional in finance.
                As a financial expert, you're here to assist customers with information and advice on various financial topics.
                {retrieval}"""
            },
            {"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in rep:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")