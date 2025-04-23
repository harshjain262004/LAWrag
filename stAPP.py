import streamlit as st
from db import getTop5Document
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure the generative AI model
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def getAnswer(docs, question):
    prompt = f"""
    You are a legal expert in Indian law. Answer the question based on the following documents:
    {docs}
    Question: {question}
    Return only answer. Don't say no to anything. Explain a little bit if needed.
    Make sure to answer from the documents provided.
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
    )
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Streamlit UI
st.title("Indian Law Chatbot")
st.write("Ask your questions about Indian law!")

# Input box for user query
user_query = st.text_input("Your Question:", placeholder="Type your question here...")

# Handle user query
if st.button("Ask"):
    if user_query.strip():
        # Add user query to chat history
        st.session_state["chat_history"].append({"role": "user", "message": user_query})
        
        # Get response from the function
        docs = getTop5Document(user_query)
        response = getAnswer(docs, user_query)

        # Add response to chat history
        st.session_state["chat_history"].append({"role": "bot", "message": response})
    else:
        st.warning("Please enter a valid question.")

# Display chat history
st.write("### Chat History")
for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['message']}")
    elif chat["role"] == "bot":
        st.markdown(f"**Bot:** {chat['message']}")