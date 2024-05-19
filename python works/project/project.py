import json
from difflib import get_close_matches
from collections import defaultdict
import pyttsx3
import requests
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

def get_duckduckgo_instant_answer(query: str) -> str:
    """Fetch instant answer from DuckDuckGo API."""
    url = f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        answer = data.get("AbstractText", "")
        if not answer:
            answer = "Sorry, I couldn't find an instant answer for that."
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

def teach_bot(knowledge_base: dict, user_input: str, new_answer: str):
    """Teach the bot a new answer."""
    knowledge_base[user_input] = new_answer
    save_knowledge_base("knowledge_base.json", knowledge_base)
    return 'Thank you for your answer. I will remember it for next time.'

def send_message():
    user_input = user_entry.get()
    chat_log.insert(tk.END, f'You: {user_input}\n')
    user_entry.delete(0, tk.END)
    
    if user_input.lower() == 'exit':
        root.quit()
        return
    elif user_input.lower() == 'clear':
        chat_log.delete(1.0, tk.END)
        return
    
    
    best_match = find_best_match(user_input, list(knowledge_base.keys()))
    if best_match:
        answer = knowledge_base[best_match]
        chat_log.insert(tk.END, f'Miab: {answer}\n')
        speak(answer)
    else:
        instant_answer = get_duckduckgo_instant_answer(user_input)
        chat_log.insert(tk.END, f'Miab (DuckDuckGo): {instant_answer}\n')
        speak(instant_answer)
        teach_bot(knowledge_base, user_input, instant_answer)

def main():
    global user_entry, chat_log, root, knowledge_base

    # Load knowledge base
    knowledge_base = load_knowledge_base("knowledge_base.json")

    # Create GUI
    root = tk.Tk()
    root.title("Chatbot-Miab")
    root.geometry("700x500")

    root.configure(bg='lightblue')  # Set background color of the window

    title_label = tk.Label(root, text="Mike's Chatbot", font=('Arial', 20, 'bold'), bg='lightblue')
    title_label.pack(pady=10)

    chat_frame = tk.Frame(root, bg='lightblue')  # Set background color of the frame
    chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    chat_log = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=60, height=20, bg='white', fg='black', font=('Arial', 10))
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    user_entry = tk.Entry(chat_frame, width=60, bg='white', fg='black', font=('Arial', 12))
    user_entry.pack(padx=10, pady=10, fill=tk.X)
    user_entry.bind("<Return>", lambda event: send_message())

    send_button = tk.Button(chat_frame, text="Send", command=send_message, bg='white', fg='black', border='2px', font=('Arial', 12))
    send_button.pack(pady=10)

    instruction_label = tk.Label(root, text='Insert your question in the text box above', font=('Arial', 12), bg='lightblue')
    instruction_label.pack(pady=10)

    # Run the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
