"""Extract key qualities and attributes from a job ad

"""
from typing import Optional
from jinja2 import Environment, FileSystemLoader
from anthropic import Anthropic

from .consts import PROMPT_TEMPLATES_DIR
from .agent_base import AgentBareMetal, AgentToolInvokeReturn
from .cv_data import Educations


env = Environment(loader=FileSystemLoader(PROMPT_TEMPLATES_DIR))


class JobAdQualityExtractor:
    """Agent that extracts key qualities and attributes from a job ad

    Args:
        client: The Anthropic client.
        model: The model to use.
        temperature: The degree of randomness in response

    """
    def __init__(self,
                 client: Anthropic,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 0.2,
                 ):
        self.agent = AgentBareMetal(
            client=client,
            model=model,
            temperature=temperature,
            instruction=env.get_template(f'{self.__class__.__name__}.txt').render()
        )

    def extract_qualities(self, text: str) -> str:
        return self.agent.run(text)


class EducationExtractor:
    """Agent that generates education summary for person

    """
    tools = ['education']
    cv_data = Educations

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words: int,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 0.2,
                 ):
        self.agent = AgentToolInvokeReturn(
            client=client,
            model=model,
            temperature=temperature,
            tools=self.tools,
            instruction=env.get_template(f'{self.__class__.__name__}.txt').render(
                relevant_qualities=relevant_qualities,
                n_words=str(n_words),
            )
        )

    def __call__(self, text: str) -> Educations:
        return self.agent.run(text)


class EmploymentExtractor:
    """Agent that generates employment summary for person

    """
    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words: int,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 0.2,
                 ):
        self.agent = AgentToolInvokeReturn(
            client=client,
            model=model,
            temperature=temperature,
            tools=['employment'],
            instruction=env.get_template(f'{self.__class__.__name__}.txt').render(
                relevant_qualities=relevant_qualities,
                n_words=str(n_words),
            )
        )

    def extract_employment(self, text: str) -> str:
        return self.agent.run(text)


class BiographyExtractor:
    """Agent that generates biography summary for person

    """
    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words: int,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 0.2,
                 ):
        self.agent = AgentToolInvokeReturn(
            client=client,
            model=model,
            temperature=temperature,
            tools=['biography', 'education', 'employment'],
            instruction=env.get_template(f'{self.__class__.__name__}.txt').render(
                relevant_qualities=relevant_qualities,
                n_words=str(n_words),
            )
        )

    def extract_biography(self, text: str) -> str:
        return self.agent.run(text)
