"""Base classes for agents that interact with the Anthropic LLMs.

In typical application, agents with specific instructions composes the base agent classes below.

"""
import json
from typing import Dict, Any, Sequence
from abc import ABC, abstractmethod

from anthropic import Anthropic
from anthropic.types import (
    Message,
    ToolUseBlock,
    ToolUseBlockParam,
    TextBlock,
    MessageParam,
    ToolResultBlockParam,
    TextBlockParam,
)

from .confs import tools_cv_data
from .semantics import get_anthropic_client, send_request_to_anthropic_message_creation
from .tools import registry_tool_funcs


class Agent(ABC):
    def __init__(self,
                 instruction: str,
                 client: Anthropic,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 1.0,
                 max_tokens: int = 4096,
                 ):
        self.anthropic_client = client
        self.system_instruction = instruction
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def run(self, text: str):
        pass


class AgentBareMetal(Agent):
    """A bare metal agent, which communicates directly with the LLM. No memory is kept.

    Args:
        instruction: The instruction to the LLM.
        api_key: The environment variable name that stores the API key for the Anthropic client.
        model: The model to use.
        temperature: The temperature for sampling.
        max_tokens: The maximum number of tokens to generate.

    """
    def __init__(self,
                 instruction: str,
                 client: Anthropic,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 1.0,
                 max_tokens: int = 4096,
                 ):
        super().__init__(
            instruction=instruction,
            client=client,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def run(self, text: str) -> str:
        """Pass text to the LLM and return the response. No memory is kept.

        """
        messages = [
            MessageParam(
                content=text,
                role='user',
            )
        ]
        response = send_request_to_anthropic_message_creation(
            client=self.anthropic_client,
            messages=messages,
            system=self.system_instruction,
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        response_message = response.content[0]
        if not isinstance(response_message, TextBlock):
            raise ValueError(f'Unexpected response type: {type(response_message)}')

        return response_message.text


class AgentToolInvokeReturn(Agent):
    """The agent that implements a semantic process

    """
    def __init__(self,
                 instruction: str,
                 client: Anthropic,
                 tools: Sequence[str],
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 1.0,
                 max_tokens: int = 4096,
                 ):
        super().__init__(
            instruction=instruction,
            client=client,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        self.tool_choice = {'type': 'any'}
        self.tools = []
        with open(tools_cv_data) as f:
            cv_data = json.load(f)
        for tool in tools:
            if tool in cv_data:
                self.tools.append(cv_data[tool])
            else:
                raise ValueError(f'Tool "{tool}" not found in CV data or functions')

    def run(self, text: str) -> Dict[str, Any]:
        """Bla bla

        """
        messages = [
            MessageParam(
                content=text,
                role='user',
            )
        ]
        response = send_request_to_anthropic_message_creation(
            client=self.anthropic_client,
            messages=messages,
            system=self.system_instruction,
            model=self.model,
            tools=self.tools,
            tool_choice=self.tool_choice,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        tool_outs = {}
        for response_message in response.content:
            assert isinstance(response_message, ToolUseBlock)

            tool_name = response_message.name
            func_kwargs = response_message.input
            tool_id = response_message.id

            tool = registry_tool_funcs.get(tool_name)
            try:
                tool_return = tool(**func_kwargs)
            except Exception as e:
                raise RuntimeError(f'Error in tool "{tool_name}" with ID "{tool_id}": {e}')
            tool_outs[tool_id] = tool_return

        return tool_outs
