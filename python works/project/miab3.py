import json
from difflib import get_close_matches
from collections import defaultdict

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
    print('Miab: Thank you for your answer. I will remember it for next time.')

def chat_bot():
    """Main function to run the chatbot."""
    knowledge_base = load_knowledge_base("knowledge_base.json")
    name = input("Hello, please insert your name and press enter to continue: ")
    print(f"Hello {name}, how can I help you today? (type 'exit' to end the conversation)")

    while True:
        user_input = input('You: ')
        if user_input.lower() == 'exit':
            print("Miab: See yaah!")
            break
        
        best_match = find_best_match(user_input, list(knowledge_base.keys()))
        if best_match:
            answer = knowledge_base[best_match]
            print(f'Miab: {answer}')
        else:
            print('Miab: Sorry, I do not have a response to your question.')
            new_answer = input('You can type an answer to teach me or "skip" to skip: ').strip()
            if new_answer.lower() == 'skip':
                continue
            else:
                teach_bot(knowledge_base, user_input, new_answer)

if __name__ == "__main__":
    chat_bot()
