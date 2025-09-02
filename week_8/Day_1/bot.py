import os
import openai
import tiktoken
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class ChatMessage(BaseModel):
    """Represents a message for OpenAI chat models."""
    role: str = Field(..., description="Role: 'system', 'user', or 'assistant'")
    content: str = Field(..., description="Content of the message")


def get_openai_client() -> openai.OpenAI:
    """
    Returns an OpenAI client using the API key from the environment.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set in environment.")
    return openai.OpenAI(api_key=api_key)


def count_tokens(messages: List[ChatMessage], model: str = "gpt-4o") -> int:
    """
    Accurately count tokens in a list of chat messages using tiktoken.

    Args:
        messages (List[ChatMessage]): List of chat messages.
        model (str): Model name for token encoding rules.

    Returns:
        int: Total number of tokens.
    """
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # Every message has a formatting overhead
        num_tokens += len(encoding.encode(message.role))
        num_tokens += len(encoding.encode(message.content))
    num_tokens += 2  # Every reply has an overhead
    return num_tokens


def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    """
    Calculates the cost of an OpenAI API call based on token usage.

    Args:
        prompt_tokens (int): Number of prompt tokens.
        completion_tokens (int): Number of completion tokens.

    Returns:
        float: Estimated cost in USD.
    """
    # Costs for GPT-4o (as of 2025)
    # $0.0005 per 1K input tokens, $0.0015 per 1K output tokens
    return (prompt_tokens * 0.0005 + completion_tokens * 0.0015) / 1000


# def main():
#     user_input = input("Enter your query: ")

#     messages = [
#         ChatMessage(role="system", content="You are a helpful assistant."),
#         ChatMessage(role="user", content=user_input)
#     ]

#     client = get_openai_client()

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[m.model_dump() for m in messages],
#         temperature=0.7
#     )

#     reply = response.choices[0].message.content
#     prompt_tokens = response.usage.prompt_tokens
#     completion_tokens = response.usage.completion_tokens
#     total_tokens = response.usage.total_tokens
#     cost = calculate_cost(prompt_tokens, completion_tokens)

#     print("\n--- Response ---")
#     print(reply)
#     print("\n--- Token Usage ---")
#     print(f"Prompt Tokens: {prompt_tokens}")
#     print(f"Completion Tokens: {completion_tokens}")
#     print(f"Total Tokens: {total_tokens}")
#     print(f"Estimated Cost: ${cost:.6f}")

def main():
    client = get_openai_client()

    print("Chat with the assistant! Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("You: ")
            if user_input.strip().lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            messages = [
                ChatMessage(role="system", content="You are a helpful assistant."),
                ChatMessage(role="user", content=user_input)
            ]

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[m.model_dump() for m in messages],
                temperature=0.7
            )

            reply = response.choices[0].message.content
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            cost = calculate_cost(prompt_tokens, completion_tokens)

            print("\nAssistant:", reply)
            print(f"\nToken Usage: Prompt={prompt_tokens}, Completion={completion_tokens}, Total={total_tokens}")
            print(f"Estimated Cost: ${cost:.6f}\n")

        except KeyboardInterrupt:
            print("\nSession ended by user (Ctrl+C).")
            break
        except Exception as e:
            print(f"An error occurred: {e}\n")



if __name__ == "__main__":
    main()
