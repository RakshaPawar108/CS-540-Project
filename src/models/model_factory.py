"""Central model management — returns LangChain chat model instances."""

import os
from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel

from src.config import SUPPORTED_MODELS, DEFAULT_TEMPERATURE

load_dotenv()


class ModelFactory:
    """Factory for creating LangChain chat model instances."""

    @staticmethod
    def get_model(model_name: str, temperature: float = DEFAULT_TEMPERATURE) -> BaseChatModel:
        """Return a LangChain ChatModel instance for the given model name.

        Args:
            model_name: Key from SUPPORTED_MODELS (e.g. "llama3.1-local").
            temperature: Sampling temperature (default 0 for deterministic).

        Returns:
            A LangChain BaseChatModel instance.

        Raises:
            ValueError: If model_name is not in SUPPORTED_MODELS.
        """
        if model_name not in SUPPORTED_MODELS:
            available = ", ".join(SUPPORTED_MODELS.keys())
            raise ValueError(
                f"Unknown model '{model_name}'. Available models: {available}"
            )

        config = SUPPORTED_MODELS[model_name]
        provider = config["provider"]
        model_id = config["model_id"]

        if provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=model_id,
                temperature=temperature,
                api_key=os.getenv("OPENAI_API_KEY"),
            )

        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=model_id,
                temperature=temperature,
                api_key=os.getenv("ANTHROPIC_API_KEY"),
            )

        elif provider == "groq":
            from langchain_groq import ChatGroq
            return ChatGroq(
                model=model_id,
                temperature=temperature,
                api_key=os.getenv("GROQ_API_KEY"),
            )

        elif provider == "ollama":
            from langchain_ollama import ChatOllama
            return ChatOllama(
                model=model_id,
                temperature=temperature,
            )

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @staticmethod
    def get_cost_info(model_name: str) -> dict:
        """Return cost metadata for a model.

        Returns:
            Dict with keys: provider, cost_per_1k_input_tokens,
            cost_per_1k_output_tokens, description.

        Raises:
            ValueError: If model_name is not in SUPPORTED_MODELS.
        """
        if model_name not in SUPPORTED_MODELS:
            raise ValueError(f"Unknown model '{model_name}'.")
        config = SUPPORTED_MODELS[model_name]
        return {
            "provider": config["provider"],
            "description": config["description"],
            "cost_per_1k_input_tokens": config["cost_per_1k_input_tokens"],
            "cost_per_1k_output_tokens": config["cost_per_1k_output_tokens"],
        }

    @staticmethod
    def list_models() -> list[str]:
        """Return list of all supported model names."""
        return list(SUPPORTED_MODELS.keys())
