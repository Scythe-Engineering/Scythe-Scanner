"""LLM client for generating summaries using OpenRouter API."""

import json
from typing import Optional

from openai import OpenAI

import color_print


def load_api_key(config_path: str = "config.json") -> Optional[str]:
    """Load OpenRouter API key from config file.

    Args:
        config_path: Path to the config.json file.

    Returns:
        API key string if found, None otherwise.
    """
    try:
        with open(config_path, 'r') as file:
            config_data = json.load(file)
            api_key = config_data.get('openrouter_api_key')
            if api_key and api_key != "your-api-key-here":
                return api_key
            else:
                color_print.print_red("API key not configured in config.json")
                return None
    except (IOError, OSError, json.JSONDecodeError) as error:
        color_print.print_red(f"Failed to load config.json: {error}")
        return None


def load_model(config_path: str = "config.json") -> Optional[str]:
    """Load model name from config file.

    Args:
        config_path: Path to the config.json file.

    Returns:
        Model name string if found, None otherwise.
    """
    try:
        with open(config_path, 'r') as file:
            config_data = json.load(file)
            model = config_data.get('model')
            if model:
                return model
            else:
                color_print.print_red("Model not configured in config.json")
                return None
    except (IOError, OSError, json.JSONDecodeError) as error:
        color_print.print_red(f"Failed to load config.json: {error}")
        return None


def generate_summary(content: str, context: str, api_key: str, model: str) -> Optional[str]:
    """Generate a summary using OpenRouter API.

    Args:
        content: The content to summarize.
        context: Context description (e.g., "file: path/to/file.py").
        api_key: OpenRouter API key.
        model: Model name to use for generation.

    Returns:
        Generated summary string if successful, None otherwise.
    """
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        prompt = f"""Generate a concise 2-3 sentence summary of the following {context}.
Focus on the main purpose, key functionality, and important details.

Content:
{content}

Summary:"""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )

        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as error:
        color_print.print_red(f"Failed to generate summary for {context}: {error}")
        return None
