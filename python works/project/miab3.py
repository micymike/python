import json
from difflib import get_close_matches
from collections import defaultdict
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()
    
def load_knowledge_base(file_path: str) -> dict:
    """Load the knowledge base from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return defaultdict(str)

def save_knowledge_base(file_path: str, knowledge_base: dict):
    """Save the knowledge base to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(knowledge_base, file, indent=2)

def find_best_match(user_question: str, questions: list) -> str:
    """Find the best match for the user's question from the knowledge base."""
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer(knowledge_base: dict, question: str) -> str:
    """Get the answer from the knowledge base."""
    return knowledge_base.get(question, "Sorry, I don't have a response to that.")

def teach_bot(knowledge_base: dict, user_input: str, new_answer: str):
    """Teach the bot a new answer."""
    knowledge_base[user_input] = new_answer
    save_knowledge_base("knowledge_base.json", knowledge_base)
    return 'Thank you for your answer. I will remember it for next time.'

def send_message(event=None):
    user_input = user_entry.get()
    chat_log.insert(tk.END, f'You: {user_input}\n')
    user_entry.delete(0, tk.END)
    
    if user_input.lower() == 'exit':
        root.quit()
        return
    
    best_match = find_best_match(user_input, list(knowledge_base.keys()))
    if best_match:
        answer = knowledge_base[best_match]
        chat_log.insert(tk.END, f'Miab: {answer}\n')
        speak(answer)
    else:
        chat_log.insert(tk.END, 'Miab: Sorry, I do not have a response to your question.\n')
        new_answer = input('You can type an answer to teach me or "skip" to skip: ').strip()
        if new_answer.lower() != 'skip':
            response = teach_bot(knowledge_base, user_input, new_answer)
            chat_log.insert(tk.END, f'Miab: {response}\n')
            speak(response)

# Load knowledge base
knowledge_base = load_knowledge_base("knowledge_base.json")

# Create GUI
root = tk.Tk()
root.title("Chatbot")

chat_frame = tk.Frame(root)
chat_frame.pack(padx=10, pady=10)

chat_log = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=60, height=20)
chat_log.pack(padx=10, pady=10)

user_entry = tk.Entry(chat_frame, width=60)
user_entry.pack(padx=10, pady=10)
user_entry.bind("<Return>", send_message)

send_button = tk.Button(chat_frame, text="Send", command=send_message)
send_button.pack(pady=10)

# Run the GUI event loop
root.mainloop()
