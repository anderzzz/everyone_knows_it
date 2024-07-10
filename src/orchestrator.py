"""Retrieve transformed data

"""
from typing import Callable, Any, Dict, Type, Tuple
from inspect import signature
from anthropic import Anthropic

from .cv_data import CVData
from .agents import (
    CVDataExtractor,
    EducationCVDataExtractor,
    EmploymentCVDataExtractor,
    BiographyCVDataExtractor,
)
from .dao import (
    DAO,
    PersonsEducationDAO,
    PersonsEmploymentDAO,
    PersonsSkillsDAO,
    PersonsPublicationsDAO,
)
_map_extractor_agents: Dict[str, Type[CVDataExtractor]] = {
    f'{EducationCVDataExtractor.cv_data.__name__}': EducationCVDataExtractor,
    f'{EmploymentCVDataExtractor.cv_data.__name__}': EmploymentCVDataExtractor,
    f'{BiographyCVDataExtractor.cv_data.__name__}': BiographyCVDataExtractor,
}
_map_extractor_daos: Dict[str, Tuple[Type[DAO]]] = {
    f'{EducationCVDataExtractor.cv_data.__name__}': (PersonsEducationDAO,),
    f'{EmploymentCVDataExtractor.cv_data.__name__}': (PersonsEmploymentDAO,),
    f'{BiographyCVDataExtractor.cv_data.__name__}': (PersonsEducationDAO, PersonsEmploymentDAO, PersonsSkillsDAO),
}


def _filter_kwargs(func: Callable, kwargs: dict) -> dict:
    return {
        k: v for k, v in kwargs.items()
        if k in signature(func).parameters
    }


class CVDataExtractionOrchestrator:
    """Orchestrate the extraction of CV data from particular data sources

    """
    def __init__(self,
                 client: Anthropic,
                 **kwargs,
                 ):
        self.client = client
        self.kwargs = kwargs

    def run(self,
            cv_data_type: str,
            data_key: Any,
            **kwargs,
            ) -> Dict[str, CVData]:
        try:
            raw_data_dao = _map_extractor_daos[cv_data_type]
        except KeyError:
            raise ValueError(f'CV data type "{cv_data_type}" not found in extractor daos')
        text = '\n\n'.join([
            dao().get(data_key) for dao in raw_data_dao
        ])

        try:
            cv_data_extractor_agent = _map_extractor_agents[cv_data_type]
        except KeyError:
            raise ValueError(f'CV data type "{cv_data_type}" not found in extractor agents')

        filtered_kwargs = _filter_kwargs(cv_data_extractor_agent.__init__, {**self.kwargs, **kwargs})
        cv_agent_instance = cv_data_extractor_agent(
            client=self.client,
            **filtered_kwargs
        )

        return cv_agent_instance(text=text)
