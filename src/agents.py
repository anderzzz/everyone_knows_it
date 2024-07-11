"""Extract key qualities and attributes from a job ad

"""
from abc import ABC, abstractmethod
from typing import Sequence, Dict
import json

from anthropic import Anthropic

from .confs import agent_model_extractor_conf
from .prompt_maker import get_prompt_for_
from .agent_base import AgentBareMetal, AgentToolInvokeReturn
from .cv_data import (
    CVData,
    Educations,
    Employments,
    Biography,
    Skills,
)


def _core_model_conf(agent_kind: str) -> Dict[str, str]:
    with open(agent_model_extractor_conf, 'r') as f:
        model_conf = json.load(f)
    try:
        return model_conf[agent_kind]
    except KeyError:
        raise ValueError(f'Agent kind "{agent_kind}" not found in model configuration file')


class JobAdQualityExtractor:
    """Agent that extracts key qualities and attributes from a job ad

    Args:
        client: The Anthropic client.

    """
    def __init__(self,
                 client: Anthropic,
                 ):
        model_core_kwargs = _core_model_conf(self.__class__.__name__)
        self.agent = AgentBareMetal(
            client=client,
            instruction=get_prompt_for_(self.__class__.__name__),
            **model_core_kwargs
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
                 **model_core_kwargs,
                 ):
        self.agent = AgentToolInvokeReturn(
            client=client,
            tools=tools,
            instruction=instruction,
            **model_core_kwargs
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
    def __call__(self, text: str) -> Dict[str, CVData]:
        pass


class EducationCVDataExtractor(CVDataExtractor):
    """Agent that generates education summary for person

    """
    tools = ['education']
    cv_data = Educations

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words_education: int,
                 ):
        model_core_kwargs = _core_model_conf(self.__class__.__name__)
        super().__init__(
            client=client,
            tools=self.tools,
            instruction=get_prompt_for_(
                self.__class__.__name__,
                relevant_qualities=relevant_qualities,
                n_words=str(n_words_education),
            ),
            **model_core_kwargs,
        )

    def __call__(self, text: str) -> Dict[str, Educations]:
        return self.agent.run(text)


class EmploymentCVDataExtractor(CVDataExtractor):
    """Agent that generates employment summary for person

    """
    tools = ['employment']
    cv_data = Employments

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words_employment: int,
                 ):
        model_core_kwargs = _core_model_conf(self.__class__.__name__)
        super().__init__(
            client=client,
            tools=self.tools,
            instruction=get_prompt_for_(
                self.__class__.__name__,
                relevant_qualities=relevant_qualities,
                n_words=str(n_words_employment),
            ),
            **model_core_kwargs,
        )

    def __call__(self, text: str) -> Dict[str, Employments]:
        return self.agent.run(text)


class SkillsCVDataExtractor(CVDataExtractor):
    """Agent that generate skills enumeration for person

    """
    cv_data = Skills
    tools = ['skills']

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_skills: int,
                 ):
        model_core_kwargs = _core_model_conf(self.__class__.__name__)
        super().__init__(
            client=client,
            tools=self.tools,
            instruction=get_prompt_for_(
                self.__class__.__name__,
                relevant_qualities=relevant_qualities,
                n_skills=str(n_skills),
            ),
            **model_core_kwargs,
        )

    def __call__(self, text: str) -> Dict[str, Skills]:
        return self.agent.run(text)


class BiographyCVDataExtractor(CVDataExtractor):
    """Agent that generates biography summary for person

    """
    tools = ['biography']
    cv_data = Biography

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words_about_me: int,
                 ):
        model_core_kwargs = _core_model_conf(self.__class__.__name__)
        super().__init__(
            client=client,
            tools=self.tools,
            instruction=get_prompt_for_(
                self.__class__.__name__,
                relevant_qualities=relevant_qualities,
                n_words=str(n_words_about_me),
            ),
            **model_core_kwargs,
        )

    def __call__(self, text: str) -> Dict[str, Biography]:
        return self.agent.run(text)
