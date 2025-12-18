from flask import Flask, jsonify, render_template, request
from rag_agent.agent import SkincareAgent
import vertexai
import os
import logging

# Setup logging so we can see errors in Cloud Console
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Initialize Vertex AI
PROJECT_ID = "skin-care-recommender"
vertexai.init(project=PROJECT_ID, location="us-central1")

# --- CRITICAL FIX: Load Agent Here ---
# This forces the model to load when the container starts,
# not when the user clicks the button.
print("Initializing SkincareAgent... this may take a minute.")
try:
    agent = SkincareAgent()
    print("SkincareAgent initialized successfully!")
except Exception as e:
    print(f"CRITICAL ERROR initializing agent: {e}")
    agent = None
# -------------------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Check if agent failed to load at startup
    if agent is None:
        return jsonify({"response": "Server Error: The AI model failed to load. Check server logs."}), 500

    try:
        data = request.json
        user_prompt = data.get("prompt", "")

        if not user_prompt:
            return jsonify({"response": "Please ask a question."})

        # Generate answer
        logging.info(f"Processing request: {user_prompt}")
        response_text = agent.get_response(user_prompt)
        
        return jsonify({"response": response_text})

    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return jsonify({"response": "Sorry, I had a glitch. Please try again."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)