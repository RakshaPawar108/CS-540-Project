"""Quick manual test — Ollama Llama 3.1 with medical questions."""

import sys
import time

sys.path.insert(0, ".")

from langchain_core.messages import HumanMessage, SystemMessage
from src.models.model_factory import ModelFactory


def test_simple_question():
    """Test with a simple medical question."""
    print("=" * 60)
    print("Test 1: Simple medical question")
    print("=" * 60)

    model = ModelFactory.get_model("llama3.1-local")

    question = "What are the common symptoms of type 2 diabetes?"
    print(f"Question: {question}\n")

    start = time.time()
    response = model.invoke([HumanMessage(content=question)])
    latency = time.time() - start

    print(f"Response:\n{response.content}\n")
    print(f"Latency: {latency:.2f}s")

    # Rough token estimate (1 token ~ 4 chars)
    input_tokens = len(question) // 4
    output_tokens = len(response.content) // 4
    print(f"Estimated tokens — input: ~{input_tokens}, output: ~{output_tokens}")


def test_structured_prompt():
    """Test with a structured system + user prompt."""
    print("\n" + "=" * 60)
    print("Test 2: Structured prompt with system message")
    print("=" * 60)

    model = ModelFactory.get_model("llama3.1-local")

    messages = [
        SystemMessage(content=(
            "You are a medical assistant. Provide accurate, concise answers "
            "to medical questions. Always recommend consulting a healthcare "
            "professional for personal medical advice."
        )),
        HumanMessage(content="What is the difference between MRI and CT scan?"),
    ]

    print(f"System: {messages[0].content}")
    print(f"User: {messages[1].content}\n")

    start = time.time()
    response = model.invoke(messages)
    latency = time.time() - start

    print(f"Response:\n{response.content}\n")
    print(f"Latency: {latency:.2f}s")

    input_tokens = sum(len(m.content) for m in messages) // 4
    output_tokens = len(response.content) // 4
    print(f"Estimated tokens — input: ~{input_tokens}, output: ~{output_tokens}")


if __name__ == "__main__":
    print("Medical Chatbot — Local Model Test")
    print(f"Available models: {ModelFactory.list_models()}\n")

    test_simple_question()
    test_structured_prompt()

    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
