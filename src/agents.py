"""Extract key qualities and attributes from a job ad

"""
from abc import ABC, abstractmethod
from typing import Dict, Type
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
)
from .tools import registry_cv_data_type_2_tool_key


def _get_core_model_conf(agent_kind: str) -> Dict[str, str]:
    with open(agent_model_extractor_conf, 'r') as f:
        model_conf = json.load(f)
    try:
        standard_model_conf = model_conf['extractors'][agent_kind]
    except KeyError:
        raise ValueError(f'Agent kind "{agent_kind}" not found in model configuration file')

    return {key: model_conf['params'][key][value] for key, value in standard_model_conf.items()}


class JobAdQualityExtractor:
    """Agent that extracts key qualities and attributes from a job ad

    Args:
        client: The Anthropic client.

    """
    NAME = 'JobAdQualityExtractor'

    def __init__(self,
                 client: Anthropic,
                 ):
        self.agent = AgentBareMetal(
            client=client,
            instruction=get_prompt_for_(self.NAME),
            **_get_core_model_conf(self.NAME)
        )

    def extract_qualities(self, text: str) -> str:
        return self.agent.run(text)


class ClearUndefinedCVDataEntries:
    """Agent that clears undefined CV data entries. Deals with the LLM issue where some
    missing entries are labelled as 'UNKNOWN', 'undefined', etc., rather than being left
    blank.

    Args:
        client: The Anthropic client.
        cv_type: The type of CV data to clear.

    """
    NAME = 'ClearUndefinedCVDataEntries'

    def __init__(self,
                 client: Anthropic,
                 cv_type: Type[CVData]
                 ):
        self.agent = AgentToolInvokeReturn(
            client=client,
            tools=registry_cv_data_type_2_tool_key.get(cv_type),
            instruction=get_prompt_for_(self.NAME),
            **_get_core_model_conf(self.NAME)
        )

    def __call__(self, cv_data_collection: Dict[str, CVData]) -> Dict[str, CVData]:
        serialized = {k: serialize_cv_data(v) for k, v in cv_data_collection.items()}
        return self.agent.run(text=json.dumps(serialized))


class CVDataExtractor(ABC):
    """Base class for CV data extractors

    """
    @abstractmethod
    def __init__(self, *args, **kwargs):
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
    NAME = 'EducationCVDataExtractor'
    cv_data = Educations

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words_education: int,
                 ):
        self.agent = AgentToolInvokeReturn(
            client=client,
            tools=registry_cv_data_type_2_tool_key.get(self.cv_data),
            instruction=get_prompt_for_(
                agent_name=self.NAME,
                relevant_qualities=relevant_qualities,
                n_words=str(n_words_education),
            ),
            **_get_core_model_conf(self.NAME),
        )

    def __call__(self, text: str) -> Dict[str, Educations]:
        return self.agent.run(text)


class EmploymentCVDataExtractor(CVDataExtractor):
    """Agent that generates employment summary for person

    """
    NAME = 'EmploymentCVDataExtractor'
    cv_data = Employments

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words_employment: int,
                 ):
        self.agent = AgentToolInvokeReturn(
            client=client,
            tools=registry_cv_data_type_2_tool_key.get(self.cv_data),
            instruction=get_prompt_for_(
                agent_name=self.NAME,
                relevant_qualities=relevant_qualities,
                n_words=str(n_words_employment),
            ),
            **_get_core_model_conf(self.NAME),
        )

    def __call__(self, text: str) -> Dict[str, Employments]:
        return self.agent.run(text)


class SkillsCVDataExtractor(CVDataExtractor):
    """Agent that generate skills enumeration for person

    """
    NAME = 'SkillsCVDataExtractor'
    cv_data = Skills

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_skills: int,
                 ):
        self.agent = AgentToolInvokeReturn(
            client=client,
            tools=registry_cv_data_type_2_tool_key.get(self.cv_data),
            instruction=get_prompt_for_(
                agent_name=self.NAME,
                relevant_qualities=relevant_qualities,
                n_skills=str(n_skills),
            ),
            **_get_core_model_conf(self.NAME),
        )

    def __call__(self, text: str) -> Dict[str, Skills]:
        return self.agent.run(text)


class BiographyCVDataExtractor(CVDataExtractor):
    """Agent that generates biography summary for person

    """
    NAME = 'BiographyCVDataExtractor'
    cv_data = Biography

    def __init__(self,
                 client: Anthropic,
                 relevant_qualities: str,
                 n_words_about_me: int,
                 ):
        self.agent = AgentToolInvokeReturn(
            client=client,
            tools=registry_cv_data_type_2_tool_key.get(self.cv_data),
            instruction=get_prompt_for_(
                agent_name=self.NAME,
                relevant_qualities=relevant_qualities,
                n_words=str(n_words_about_me),
            ),
            **_get_core_model_conf(self.NAME),
        )

    def __call__(self, text: str) -> Dict[str, Biography]:
        return self.agent.run(text)


class BiographyCVDataExtractorWithClearUndefined(CVDataExtractor):
    """Agent that generates biography summary for person, ensuring there are no undefined entries

    """
    NAME = 'BiographyCVDataExtractorWithClearUndefined'
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
