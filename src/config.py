"""Shared configuration for the Medical Chatbot project."""

SUPPORTED_MODELS = {
    # OpenAI models
    "gpt-4o": {
        "provider": "openai",
        "model_id": "gpt-4o",
        "description": "GPT-4o — flagship multimodal model",
        "cost_per_1k_input_tokens": 0.0025,
        "cost_per_1k_output_tokens": 0.01,
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "model_id": "gpt-4o-mini",
        "description": "GPT-4o Mini — fast and affordable",
        "cost_per_1k_input_tokens": 0.00015,
        "cost_per_1k_output_tokens": 0.0006,
    },
    # Anthropic models
    "claude-sonnet-4.5": {
        "provider": "anthropic",
        "model_id": "claude-sonnet-4-5-20250929",
        "description": "Claude Sonnet 4.5 — balanced performance",
        "cost_per_1k_input_tokens": 0.003,
        "cost_per_1k_output_tokens": 0.015,
    },
    "claude-haiku-4.5": {
        "provider": "anthropic",
        "model_id": "claude-haiku-4-5-20251001",
        "description": "Claude Haiku 4.5 — fast and cheap",
        "cost_per_1k_input_tokens": 0.0008,
        "cost_per_1k_output_tokens": 0.004,
    },
    # Groq (free tier)
    "llama3.1-groq": {
        "provider": "groq",
        "model_id": "llama-3.3-70b-versatile",
        "description": "Llama 3.3 70B via Groq — free cloud inference",
        "cost_per_1k_input_tokens": 0.0,
        "cost_per_1k_output_tokens": 0.0,
    },
    # Local Ollama
    "llama3.1-local": {
        "provider": "ollama",
        "model_id": "llama3.1",
        "description": "Llama 3.1 8B via Ollama — local, free",
        "cost_per_1k_input_tokens": 0.0,
        "cost_per_1k_output_tokens": 0.0,
    },
}

DEFAULT_MODEL = "llama3.1-local"
DEFAULT_TEMPERATURE = 0
