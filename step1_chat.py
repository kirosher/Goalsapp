"""
Step 1: talk to a cloud model from Python.
No personality, no memory yet. Just checking that everything works.

Run from VS Code: open this file and press F5 (uses .vscode/launch.json),
or click the "Run Python File" button. Either way it runs in the terminal,
so you can type your messages.
"""

import sys

try:
    import httpx  # installed together with ollama
    import ollama
except ImportError:
    sys.exit(
        "The 'ollama' package isn't installed for this Python:\n"
        f"  {sys.executable}\n"
        "Fix: in the VS Code terminal run\n"
        f'  "{sys.executable}" -m pip install -r requirements.txt\n'
        "or pick the right interpreter (Ctrl+Shift+P -> 'Python: Select Interpreter')."
    )

MODEL = "gemma4:cloud"  # copy the exact name from ollama.com/search?c=cloud

messages = []
print("Type 'quit' to stop.")

while True:
    try:
        user_text = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
        # EOFError happens when the script runs somewhere you can't type
        # (e.g. the read-only Output panel). Run it in the terminal instead.
        print()
        break
    if user_text.lower() == "quit":
        break
    if not user_text:
        continue

    messages.append({"role": "user", "content": user_text})

    reply = ""
    print("Bot: ", end="", flush=True)
    try:
        # stream=True prints the answer word by word instead of all at once
        stream = ollama.chat(model=MODEL, messages=messages, think=False, stream=True)
        for chunk in stream:
            piece = chunk["message"]["content"]
            print(piece, end="", flush=True)
            reply += piece
    except (ConnectionError, httpx.ConnectError):
        print("\nCan't reach Ollama. Start the Ollama app (or run 'ollama serve') and try again.")
        messages.pop()
        continue
    except ollama.ResponseError as e:
        print(f"\nOllama error: {e.error}")
        print(f"Check the model name '{MODEL}' and, for cloud models, run 'ollama signin'.")
        messages.pop()
        continue
    print()

    messages.append({"role": "assistant", "content": reply})
