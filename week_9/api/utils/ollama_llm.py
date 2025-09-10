# week_9/api/utils/ollama_llm.py

"""Ollama integration for local LLMs."""

from langchain_community.chat_models import ChatOllama
from week_9.api.constants import OLLAMA_MODEL, OLLAMA_TEMPERATURE


def get_ollama_llm(model: str = OLLAMA_MODEL, temperature: float = OLLAMA_TEMPERATURE):
    """Return a configured Ollama LLM client."""
    return ChatOllama(model=model, temperature=temperature)
