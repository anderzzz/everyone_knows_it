"""Bla bla

"""
import json
from typing import Optional, Sequence
from abc import ABC, abstractmethod

from anthropic.types import (
    Message,
    ToolUseBlock,
    ToolUseBlockParam,
    TextBlock,
    MessageParam,
    ToolResultBlockParam,
    TextBlockParam,
)

from consts import CONF_CV_DATA, CONF_FUNCS
from semantics import get_anthropic_client, send_request_to_anthropic_message_creation
from tools import get_tool


class Agent(ABC):
    """Base class for agents

    """
    def __init__(self,
                 instruction: str,
                 api_key: str,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 1.0,
                 max_tokens: int = 4096,
                 ):
        self.anthropic_client = get_anthropic_client(api_key)
        self.system_instruction = instruction
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def run(self, text: str):
        pass


class AgentBareMetal(Agent):
    """A bare metal agent, which communicates directly with the LLM

    """
    def __init__(self,
                 instruction: str,
                 api_key: str,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 1.0,
                 max_tokens: int = 4096,
                 ):
        super().__init__(
            instruction=instruction,
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def run(self, text: str) -> str:
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
                 api_key: str,
                 tools: Sequence[str],
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 1.0,
                 max_tokens: int = 4096,
                 ):
        super().__init__(
            instruction=instruction,
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        self.tool_choice = {'type': 'any'}
        self.tools = []
        with open(CONF_CV_DATA) as f:
            cv_data = json.load(f)
        with open(CONF_FUNCS) as f:
            funcs = json.load(f)
        for tool in tools:
            if tool in cv_data:
                self.tools.append(cv_data[tool])
            elif tool in funcs:
                self.tools.append(funcs[tool])
            else:
                raise ValueError(f'Tool "{tool}" not found in CV data or functions')

    def run(self, text: str):
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

            tool = get_tool(tool_name)
            try:
                tool_return = tool(**func_kwargs)
            except Exception as e:
                raise RuntimeError(f'Error in tool "{tool_name}" with ID "{tool_id}": {e}')
            tool_outs[tool_id] = tool_return

        return tool_outs
