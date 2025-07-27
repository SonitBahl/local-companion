import ollama
import subprocess

MODEL_NAME = "mistral"

def ensure_model_exists(model_name):
    models = ollama.list()["models"]
    if not any(m["model"].startswith(model_name) for m in models):
        subprocess.run(["ollama", "pull", model_name], check=True)

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

def chat():
    ensure_model_exists(MODEL_NAME)
    print("AI 🤖: Hi there! I'm your cheerful AI companion. Let's talk!")

    while True:
        user_input = input("You 🧑: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("AI 🤖: Alright! Take care and keep smiling")
            break

        conversation_history.append({"role": "user", "content": user_input})

        response = ollama.chat(model=MODEL_NAME, messages=conversation_history)
        reply = response["message"]["content"]

        print("AI 🤖:", reply)
        conversation_history.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    chat()
