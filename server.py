from flask import Flask, render_template, request, jsonify
import ollama
import subprocess

app = Flask(__name__)

MODEL_NAME = "mistral"
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a cheerful, friendly, and supportive AI companion. "
            "You greet warmly, stay positive, and try to remember what the user says during this conversation. "
            "If the user feels low, cheer them up gently with humor or encouragement."
        )
    }
]

def ensure_model_exists(model_name):
    models = ollama.list()["models"]
    if not any(m["model"].startswith(model_name) for m in models):
        subprocess.run(["ollama", "pull", model_name], check=True)

ensure_model_exists(MODEL_NAME)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    conversation_history.append({"role": "user", "content": user_input})

    response = ollama.chat(model=MODEL_NAME, messages=conversation_history)
    reply = response["message"]["content"]
    conversation_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
