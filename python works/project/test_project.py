import pytest
from project import load_knowledge_base, find_best_match, get_duckduckgo_instant_answer

def test_load_knowledge_base():
    knowledge_base = load_knowledge_base("test_knowledge_base.json")
    assert isinstance(knowledge_base, dict)
    assert "hello" in knowledge_base
    assert knowledge_base["hello"] == "hello"

def test_find_best_match():
    questions = ["What is your name?", "How are you?", "What is the capital of France?"]
    best_match = find_best_match("What is your name", questions)
    assert best_match == "What is your name?"

    best_match = find_best_match("How are you doing?", questions)
    assert best_match == "How are you?"

    best_match = find_best_match("What is your favorite color?", questions)
    assert best_match is None

def test_get_duckduckgo_instant_answer():
    answer = get_duckduckgo_instant_answer("What is the capital of France?")
    assert isinstance(answer, str)
    assert len(answer) > 0

if __name__ == "__main__":
    pytest.main()
