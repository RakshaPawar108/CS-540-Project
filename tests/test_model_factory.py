"""Smoke tests for ModelFactory."""

import pytest
from src.models.model_factory import ModelFactory


def test_get_model_ollama_returns_valid_object():
    """get_model('llama3.1-local') should return a LangChain chat model."""
    model = ModelFactory.get_model("llama3.1-local")
    assert model is not None
    assert hasattr(model, "invoke")


def test_get_cost_info_returns_expected_fields():
    """get_cost_info should return provider, description, and cost fields."""
    info = ModelFactory.get_cost_info("gpt-4o")
    assert "provider" in info
    assert "description" in info
    assert "cost_per_1k_input_tokens" in info
    assert "cost_per_1k_output_tokens" in info
    assert info["provider"] == "openai"


def test_get_cost_info_local_is_free():
    """Local Ollama model should have zero cost."""
    info = ModelFactory.get_cost_info("llama3.1-local")
    assert info["cost_per_1k_input_tokens"] == 0.0
    assert info["cost_per_1k_output_tokens"] == 0.0


def test_invalid_model_raises_value_error():
    """Unknown model name should raise ValueError."""
    with pytest.raises(ValueError, match="Unknown model"):
        ModelFactory.get_model("nonexistent-model")


def test_list_models_returns_all():
    """list_models should return all configured model names."""
    models = ModelFactory.list_models()
    assert "llama3.1-local" in models
    assert "gpt-4o" in models
    assert len(models) >= 6
