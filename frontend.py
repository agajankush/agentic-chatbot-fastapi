# 1. Setup UI with streamlit (model provider, model, system prompt, web search, query)
import streamlit as st

st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
st.title("AI Chatbot Agents")
st.write("Creat and Interact with the AI Agents!")

system_prompt = st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here....")

MODEL_NAMES_GROQ = ["llama3-70b-8192", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-40-mini"]

provider=st.radio("Select Provider: ", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model=st.selectbox("Selected Groq Model: ",  MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model=st.selectbox("Selected OpenAI Model: ",  MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area("Enter your query: ", height=150, placeholder="Ask Anything")

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent!"):
    if user_query.strip():
        # 2. Connect with backend via URL
        import requests
        payload = {
            "model_name": selected_model, 
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        response = requests.post(API_URL, json=payload)

        # Get response from the backend
        # response="Hi, this is a fixed dummy response"
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(response_data)
