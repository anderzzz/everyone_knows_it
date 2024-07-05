"""Semantic interfaces to LLMs.

"""
import os
from typing import List, Dict, Optional

from anthropic import Anthropic
from anthropic.types import Message


def get_anthropic_client(env_var: str) -> Anthropic:
    """Get an Anthropic client from an environment variable.

    Args:
        env_var: The environment variable to use for the API key.

    Returns:
        An Anthropic client.

    """
    return Anthropic(api_key=os.getenv(env_var))


def send_request_to_anthropic_message_creation(
        client: Anthropic,
        messages: List[Dict],
        system: Optional[str] = None,
        model: str = 'claude-3-haiku-20240307',
        tools: Optional[List[str]] = None,
        tool_choice: Optional[Dict] = {'type': 'auto'},
        max_tokens: int = 256,
        temperature: float = 1.0,
) -> Message:
    kwargs = {
        'model': model,
        'system': system,
        'messages': messages,
        'tools': tools,
        'tool_choice': tool_choice,
        'max_tokens': max_tokens,
        'temperature': temperature,
    }
    if tools is None:
        del kwargs['tools']
        del kwargs['tool_choice']

    try:
        antrophic_message = client.messages.create(**kwargs)
    except Exception as e:
        raise ValueError(f'Error in sending request to Anthropic: {e}')

    return antrophic_message
