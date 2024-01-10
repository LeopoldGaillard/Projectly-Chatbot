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
    url = f"http://127.0.0.1:49168/projectly/docs/rag_search/{query}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Unable to fetch data"}

    res = response.json()
    context = ""
    highlights = []

    if res != []:
        for i, item in enumerate(res, start=1):
            data = item["_source"]
            context += f"Title: {data['title']}\nDescription: {data['description']}\nContent: {data['content']}\n\n"
            
            if i <= 2:
                test_len = context

            # Traitement des highlights
            highlight = item.get('highlight', {})
            text_parts = [' '.join(highlight.get(field, [])) for field in ['title', 'description', 'content']]
            highlights.append(' '.join(text_parts))

        if len(test_len) <= 3500:
            return f"Potentially relevant context : {test_len}" if test_len else ""

        all_highlights = ' '.join(highlights)
        return f"Potentially relevant context : {all_highlights[:7000]}" if all_highlights else ""
    else:
        return "No relevant context found."