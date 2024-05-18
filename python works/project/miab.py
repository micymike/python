import ChatBot
import ChatterBotCorpusTrainer, ListTrainer

# Instantiate the chatbot
chatbot = ChatBot(
    "Advance MIAB",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.TimeLogicAdapter",
    ],
    database_uri="sqlite:///database.sqlite3"
)

# Custom conversation training
custom_conversations = [
    "Hello", "Hi there! How can I help you today?",
    "What is your name?", "My name is Advance MIAB. I am a chatbot designed to help you with your banking needs."
]

# New trainer for the chatbot
list_trainer = ListTrainer(chatbot)
# Training the chatbot with custom conversations
list_trainer.train(custom_conversations)

# Training the chatbot based on English corpus
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train("chatterbot.corpus.english")

# Function to start the chatbot
def start():
    print("Jambo, Welcome to Advance MIAB. Type 'exit' to end this conversation.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("See yaah!")
                break
            bot_response = chatbot.get_response(user_input)
            print(f"Miab: {bot_response}")
        except (KeyboardInterrupt, EOFError, SystemExit):
            print("\nSee yaah!")
            break

if __name__ == "__main__":
    start()
