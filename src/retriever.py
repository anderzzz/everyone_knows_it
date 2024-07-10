"""Retrieve transformed data

"""
from typing import Callable, Any
from anthropic import Anthropic

from .pipeline import Pipeline, PipelineStep
from .registry import Registry
from .drl import (
    registry_persons,
    registry_job_ads,
    registry_form_templates,
    registry_form_templates_toc,
)
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


class RetrieverBuilder:
    """Bla bla

    """
    def __init__(self,
                 client: Anthropic,
                 data_getter: Callable,
                 **kwargs,
                 ):
        self.client = client
        self.data_getter = data_getter
        self.kwargs = kwargs

    def build(self,
              form_template: str,
              data_key: Any,
              ) -> Pipeline:
        try:
            required_cv_data_types = registry_form_templates_toc.get(form_template)['required_cv_data_types']
        except KeyError:
            raise ValueError(f'Form template "{form_template}" not found in form data')

        for cv_data_type in required_cv_data_types:
            try:
                cv_data_extractor_agent = _map_extractor_agents[cv_data_type]
            except KeyError:
                raise ValueError(f'CV data type "{cv_data_type}" not found in extractor agents')

            cv_agent_instance = cv_data_extractor_agent(
                client=self.client,
                **self.kwargs
            )
