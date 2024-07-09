"""Extract key qualities and attributes from a job ad

"""
from abc import ABC, abstractmethod
from typing import Sequence
from jinja2 import Environment, FileSystemLoader
from anthropic import Anthropic

from .consts import PROMPT_TEMPLATES_DIR
from .agent_base import AgentBareMetal, AgentToolInvokeReturn
from .cv_data import (
    CVData,
    Educations,
    Employments,
    Biography
)


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


class CVDataExtractor(ABC):
    """Agent that extracts data for CV

    """
    def __init__(self,
                 client: Anthropic,
                 instruction: str,
                 tools: Sequence[str],
                 model: str,
                 temperature: float,
                 ):
        self.agent = AgentToolInvokeReturn(
            client=client,
            model=model,
            temperature=temperature,
            tools=tools,
            instruction=instruction
        )

    @property
    @abstractmethod
    def tools(self) -> Sequence[str]:
        pass

    @property
    @abstractmethod
    def cv_data(self) -> CVData:
        pass

    @abstractmethod
    def __call__(self, text: str) -> CVData:
        pass


class EducationCVDataExtractor(CVDataExtractor):
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
        super().__init__(
            client=client,
            tools=self.tools,
            model=model,
            temperature=temperature,
            instruction=env.get_template(f'{self.__class__.__name__}.txt').render(
                relevant_qualities=relevant_qualities,
                n_words=str(n_words),
            )
        )

    def __call__(self, text: str) -> Educations:
        return self.agent.run(text)


class EmploymentCVDataExtractor(CVDataExtractor):
    """Agent that generates employment summary for person

    """
    tools = ['employment']
    cv_data = Employments

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words: int,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 0.2,
                 ):
        super().__init__(
            client=client,
            tools=['employment'],
            model=model,
            temperature=temperature,
            instruction=env.get_template(f'{self.__class__.__name__}.txt').render(
                relevant_qualities=relevant_qualities,
                n_words=str(n_words),
            )
        )

    def __call__(self, text: str) -> str:
        return self.agent.run(text)


class BiographyCVDataExtractor(CVDataExtractor):
    """Agent that generates biography summary for person

    """
    tools = ['biography', 'education', 'employment']
    cv_data = Biography

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words: int,
                 model: str = 'claude-3-haiku-20240307',
                 temperature: float = 0.2,
                 ):
        super().__init__(
            client=client,
            tools=self.tools,
            model=model,
            temperature=temperature,
            instruction=env.get_template(f'{self.__class__.__name__}.txt').render(
                relevant_qualities=relevant_qualities,
                n_words=str(n_words),
            )
        )

    def __call__(self, text: str) -> Biography:
        return self.agent.run(text)
