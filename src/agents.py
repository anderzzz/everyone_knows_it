"""Extract key qualities and attributes from a job ad

"""
from abc import ABC, abstractmethod
from typing import Sequence, Dict, Type
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
    serialize_cv_data,
    dataclass_to_str,
)
from .tools import registry_cv_data_type_2_tool_key


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


class ClearUndefinedCVDataEntries:
    """Bla bla

    """
    def __init__(self,
                 client: Anthropic,
                 cv_type: Type[CVData]
                 ):
        model_core_kwargs = _core_model_conf(self.__class__.__name__)
        self.agent = AgentToolInvokeReturn(
            client=client,
            tools=registry_cv_data_type_2_tool_key.get(cv_type),
            instruction=get_prompt_for_(
                self.__class__.__name__,
            ),
            **model_core_kwargs
        )

    def __call__(self, cv_data_collection: Dict[str, CVData]) -> Dict[str, CVData]:
        serialized = {k: serialize_cv_data(v) for k, v in cv_data_collection.items()}
        return self.agent.run(text=json.dumps(serialized))


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
    def cv_data(self) -> CVData:
        pass

    @abstractmethod
    def __call__(self, text: str) -> Dict[str, CVData]:
        pass


class EducationCVDataExtractor(CVDataExtractor):
    """Agent that generates education summary for person

    """
    cv_data = Educations

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words_education: int,
                 ):
        model_core_kwargs = _core_model_conf(self.__class__.__name__)
        super().__init__(
            client=client,
            tools=registry_cv_data_type_2_tool_key.get(self.cv_data),
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
    cv_data = Employments

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words_employment: int,
                 ):
        model_core_kwargs = _core_model_conf(self.__class__.__name__)
        super().__init__(
            client=client,
            tools=registry_cv_data_type_2_tool_key.get(self.cv_data),
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

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_skills: int,
                 ):
        model_core_kwargs = _core_model_conf(self.__class__.__name__)
        super().__init__(
            client=client,
            tools=registry_cv_data_type_2_tool_key.get(self.cv_data),
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
    cv_data = Biography

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words_about_me: int,
                 ):
        model_core_kwargs = _core_model_conf(self.__class__.__name__)
        super().__init__(
            client=client,
            tools=registry_cv_data_type_2_tool_key.get(self.cv_data),
            instruction=get_prompt_for_(
                self.__class__.__name__,
                relevant_qualities=relevant_qualities,
                n_words=str(n_words_about_me),
            ),
            **model_core_kwargs,
        )

    def __call__(self, text: str) -> Dict[str, Biography]:
        return self.agent.run(text)


class BiographyCVDataExtractorWithClearUndefined:
    """Bla bla

    """
    cv_data = Biography

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words_about_me: int,
                 ):
        self.extractor = BiographyCVDataExtractor(
            client=client,
            relevant_qualities=relevant_qualities,
            n_words_about_me=n_words_about_me,
        )
        self.clear_undefined = ClearUndefinedCVDataEntries(
            client=client,
            cv_type=self.cv_data,
        )

    def __call__(self, text: str) -> Dict[str, Biography]:
        return self.clear_undefined(self.extractor(text))
