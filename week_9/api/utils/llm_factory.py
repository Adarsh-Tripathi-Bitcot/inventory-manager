"""Factory to return the correct LLM instance based on provider string."""

import logging
from langchain_openai import ChatOpenAI
from week_9.api.utils.ollama_llm import get_ollama_llm
from week_9.api.constants import (
    OPENAI_CHAT_MODEL,
    OPENAI_TEMPERATURE,
    OLLAMA_MODEL,
    OLLAMA_TEMPERATURE,
)

logger = logging.getLogger(__name__)


def get_llm(provider: str = "openai"):
    """
    Return an LLM instance based on the provider name.

    Args:
        provider (str): Name of the LLM provider ('openai' or 'ollama').

    Returns:
        LLM: Configured LLM client.
    """
    provider = provider.lower().strip()

    if provider == "ollama":
        logger.info("Using Ollama model via LLM Factory...")
        return get_ollama_llm(model=OLLAMA_MODEL, temperature=OLLAMA_TEMPERATURE)

    logger.info("Using OpenAI model via LLM Factory...")
    return ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=OPENAI_TEMPERATURE)
