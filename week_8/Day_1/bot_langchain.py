# week_8/Day_1/bot_langchain.py
import os
import sys
from langchain_openai import ChatOpenAI  
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from api.constants import OPENAI_CHAT_MODEL
from dotenv import load_dotenv

# Ensure Python can find the week_8 package no matter where we run from
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# Load environment variables (expects OPENAI_API_KEY)
load_dotenv()

# Initialize LangChain Chat model
chat_model = ChatOpenAI(
    model_name=OPENAI_CHAT_MODEL,
    temperature=0.7
)

# Build a chat prompt template (system + user message)
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{user_input}")
])

# Output parser
output_parser = StrOutputParser()

# LCEL pipeline: prompt → model → parser
chain = chat_prompt | chat_model | output_parser


def main():
    print("Chat with LangChain assistant! Type 'exit' or 'quit' to stop.\n")
    while True:
        try:
            user_input = input("You: ")
            if user_input.strip().lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            # Run the chain with user input
            reply = chain.invoke({"user_input": user_input})

            print("\nAssistant:", reply, "\n")

        except KeyboardInterrupt:
            print("\nSession ended by user (Ctrl+C).")
            break
        except Exception as e:
            print(f"An error occurred: {e}\n")


if __name__ == "__main__":
    main()
