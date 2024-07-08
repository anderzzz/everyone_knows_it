"""Extract key qualities and attributes from a job ad

"""
from typing import Optional
from jinja2 import Environment, FileSystemLoader

from .consts import PROMPT_TEMPLATES_DIR
from .agent_base import AgentBareMetal, AgentToolInvokeReturn
from .cv_data import Educations


env = Environment(loader=FileSystemLoader(PROMPT_TEMPLATES_DIR))


class JobAdQualityExtractor:
    """Agent that extracts key qualities and attributes from a job ad

    """
    def __init__(self,
                 model: str = 'claude-3-haiku-20240307',
                 api_key: str = 'ANTHROPIC_API_KEY',
                 ):
        self.agent = AgentBareMetal(
            api_key=api_key,
            model=model,
            instruction=env.get_template(f'{self.__class__.__name__}.txt').render()
        )

    def extract_qualities(self, text: str) -> str:
        return self.agent.run(text)


class EducationExtractor:
    """Agent that generates education summary for person

    """
    def __init__(self,
                 relevant_qualities: str,
                 n_words: int,
                 model: str = 'claude-3-haiku-20240307',
                 api_key: str = 'ANTHROPIC_API_KEY',
                 ):
        self.agent = AgentToolInvokeReturn(
            api_key=api_key,
            model=model,
            tools=['education'],
            instruction=env.get_template(f'{self.__class__.__name__}.txt').render(
                relevant_qualities=relevant_qualities,
                n_words=str(n_words),
            )
        )

    def extract_education(self, text: str) -> Educations:
        return self.agent.run(text)
