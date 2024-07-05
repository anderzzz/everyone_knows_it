"""Bla bla

"""
import json
from typing import Optional, Sequence

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


class Agent:
    """The agent that implements a semantic process

    """
    def __init__(self,
                 instruction: str,
                 api_key: str,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 1.0,
                 max_tokens: int = 4096,
                 tools: Optional[Sequence[str]] = None,
                 tool_choice: Optional[str] = 'auto',
                 ):
        self.anthropic_client = get_anthropic_client(api_key)
        self.system_instruction = instruction
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.tool_choice = {'type': tool_choice}
        self.tools = []
        if tools is not None:
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
        _tool_use = False
        _content_obj = None

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
        for response_message in response.content:
            print (response_message)
            if isinstance(response_message, TextBlock):
                _content_obj = TextBlockParam(**response_message.model_dump())
            elif isinstance(response_message, ToolUseBlock):
                _tool_use = True
                _content_obj = ToolUseBlockParam(**response_message.model_dump())
            else:
                raise ValueError(f'Unknown response type: {response_message.__class__.__name__}')

            messages.append(
                MessageParam(
                    content=[_content_obj],
                    role='assistant',
                )
            )

            if _tool_use:
                tool_name = response_message.name
                func_kwargs = response_message.input
                tool_id = response_message.id

                tool = get_tool(tool_name)
                try:
                    tool_return = tool(**func_kwargs)
                except Exception as e:
                    raise RuntimeError(f'Error in tool "{tool_name}" with ID "{tool_id}": {e}')

                print (tool_return)

        return 'hello'