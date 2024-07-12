"""The orchestrator combines the agents and DAOs to extract CV data.

This is where the association between the CV data types and the DAOs
as well as the CV data extractor agents is made.

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
    BiographyCVDataExtractorWithClearUndefined,
    SkillsCVDataExtractor,
)
from .dao import (
    DAO,
    PersonsEducationDAO,
    PersonsEmploymentDAO,
    PersonsSkillsDAO,
    PersonsPublicationsDAO,
    PersonsMusingsDAO,
)

_map_extractor_agents: Dict[str, Type[CVDataExtractor]] = {
    f'{EducationCVDataExtractor.cv_data.__name__}': EducationCVDataExtractor,
    f'{EmploymentCVDataExtractor.cv_data.__name__}': EmploymentCVDataExtractor,
    f'{BiographyCVDataExtractor.cv_data.__name__}': BiographyCVDataExtractorWithClearUndefined,
    f'{SkillsCVDataExtractor.cv_data.__name__}': SkillsCVDataExtractor,
}
"""Map CV data types to CV data extractor agents

"""

_map_extractor_daos: Dict[str, Tuple[Type[DAO]]] = {
    f'{EducationCVDataExtractor.cv_data.__name__}': (PersonsEducationDAO,),
    f'{EmploymentCVDataExtractor.cv_data.__name__}': (PersonsEmploymentDAO,),
    f'{BiographyCVDataExtractor.cv_data.__name__}': (PersonsEducationDAO, PersonsEmploymentDAO, PersonsMusingsDAO),
    f'{SkillsCVDataExtractor.cv_data.__name__}': (PersonsEducationDAO, PersonsEmploymentDAO, PersonsSkillsDAO),
}
"""Map CV data types to DAOs that provide raw data for the CV data extractor agents

This allows for a pre-filtering of raw data that are passed to the extractors. For example,
if the extractor is tailored to extract education data, then only the education DAO is used.
This is strictly not needed since the Extractor LLM should be able to do the filtering itself,
though at a higher token cost.

"""


def _filter_kwargs(func: Callable, kwargs: Dict) -> Dict:
    """Filter keyword arguments to match the function signature"""
    return {
        k: v for k, v in kwargs.items()
        if k in signature(func).parameters
    }


class CVDataExtractionOrchestrator:
    """Orchestrate the extraction of CV data from particular data sources

    The extraction process invokes a CV data extractor agent to process the raw data
    associated with a particular data key.

    Args:
        client: The Anthropic client.
        **kwargs: Additional keyword arguments to pass to the CV data extractor agents.
            These can be overridden by the keyword arguments passed to the `run` method.

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
        """Run the extraction process

        Args:
            cv_data_type (str): The type of CV data to extract.
            data_key (Any): The key to the raw data.
            **kwargs: Additional keyword arguments to pass to the CV data extractor agents.

        Returns:
            Dict[str, CVData]: The extracted CV data, keyed on a unique identifier.

        """
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
