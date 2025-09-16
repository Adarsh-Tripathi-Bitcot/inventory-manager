# week_8/Day_1/bot_langchain.py
import os
import sys
import logging
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from api.constants import OPENAI_CHAT_MODEL, OPENAI_TEMPERATURE

# Ensure Python can find the week_8 package no matter where we run from
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Load environment variables (expects OPENAI_API_KEY)
load_dotenv()

# Initialize LangChain Chat model
chat_model = ChatOpenAI(
    model_name=OPENAI_CHAT_MODEL,
    temperature=OPENAI_TEMPERATURE,
)

# Build a chat prompt template (system + user message)
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{user_input}"),
])

# Output parser
output_parser = StrOutputParser()

# LCEL pipeline: prompt → model → parser
chain = chat_prompt | chat_model | output_parser


def get_user_input() -> str:
    """Prompt the user for input and return it."""
    return input("You: ").strip()


def process_input(user_input: str) -> str:
    """Process valid user input through the chain."""
    return chain.invoke({"user_input": user_input})


def display_output(reply: str) -> None:
    """Display assistant's reply."""
    logging.info(f"Assistant: {reply}")


def main():
    logging.info("Chat with LangChain assistant! Type 'exit' or 'quit' to stop.\n")
    while True:
        try:
            user_input = get_user_input()

            # Handle exit command
            if user_input.lower() in {"exit", "quit"}:
                logging.info("Goodbye!")
                break

            # Validate non-empty input
            if not user_input:
                logging.warning("Empty input ignored. Please type something.")
                continue

            # Process and display reply
            reply = process_input(user_input)
            display_output(reply)

        except KeyboardInterrupt:
            logging.info("Session ended by user (Ctrl+C).")
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
