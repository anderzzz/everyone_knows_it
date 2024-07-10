"""Retrieve transformed data

"""
from typing import Callable, Any
from anthropic import Anthropic

from .cv_data import CVData
from .agents import (
    EducationCVDataExtractor,
    EmploymentCVDataExtractor,
    BiographyCVDataExtractor,
)
_map_extractor_agents = {
    f'{EducationCVDataExtractor.cv_data}': EducationCVDataExtractor,
    f'{EmploymentCVDataExtractor.cv_data}': EmploymentCVDataExtractor,
    f'{BiographyCVDataExtractor.cv_data}': BiographyCVDataExtractor,
}


class CVDataExtractionOrchestrator:
    """Orchestrate the extraction of CV data from particular data sources

    """
    def __init__(self,
                 client: Anthropic,
                 data_getter: Callable,
                 **kwargs,
                 ):
        self.client = client
        self.data_getter = data_getter
        self.kwargs = kwargs

    def run(self,
            cv_data_type: str,
            data_key: Any,
            ) -> CVData:
        try:
            cv_data_extractor_agent = _map_extractor_agents[cv_data_type]
        except KeyError:
            raise ValueError(f'CV data type "{cv_data_type}" not found in extractor agents')

        cv_agent_instance = cv_data_extractor_agent(
            client=self.client,
            **self.kwargs
        )

        return cv_agent_instance(text=self.data_getter(data_key))
