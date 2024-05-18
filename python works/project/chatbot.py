import nltk # type: ignore
from nltk.chat.util import Chat, reflections # type: ignore

patterns = [
    [r'what is your name?', ['My name is Chatbot Miab, created by Michael Moses. What is your name?']],
    [r'how are you?', ['I am doing good. What about you?']],
    [r'what can you do?', ['I can answer any sort of questions. What else would you like to know?']],
    [r'what is your favorite color?', ['My favorite color is blue. What is your favorite color?']],
    [r'what is your favorite food?', ['My favorite food is Ugali. What is your favorite food?']],
    [r'what is your favorite animal?', ['My favorite animal is a cat. What is your favorite animal?']],
    [r'what is your favorite sport?', ['Michael didn\'t create me to have a favorite sport']],
    [r'what is your favorite movie?', ['Michael didn\'t create me to have a favorite movie']],
    [r'sorry', ['It\'s alright, no problem at all. What can I do for you?']],
    [r'tell me a joke', ['like how your, life is a joke']]
]

def chatbot():
    print("Jambo, I am Miab, created by Michael Moses. How can I assist you?")
    chat = Chat(patterns, reflections)
    chat.converse()

if __name__ == "__main__":
    chatbot()
