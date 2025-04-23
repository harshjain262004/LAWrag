from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from db import getTop5Document
import google.generativeai as genai

app = Flask(__name__)

# Load environment variables
load_dotenv()

def getAnswer(docs, question):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Extract the question from the request
        data = request.get_json()
        user_query = data.get("question", "").strip()

        if not user_query:
            return jsonify({"error": "Invalid question"}), 400

        # Get top 5 documents and generate an answer
        docs = getTop5Document(user_query)
        response = getAnswer(docs, user_query)

        return jsonify({"answer": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True)