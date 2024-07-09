"""

"""
import json

from .consts import FORM_DATA
from .agents import (
    EducationExtractor,
    EmploymentExtractor,
    BiographyExtractor,
)
_map_extractor_agents = {
    f'{EducationExtractor.cv_data}': EducationExtractor,
    f'{EmploymentExtractor.cv_data}': EmploymentExtractor,
    f'{BiographyExtractor.cv_data}': BiographyExtractor,
}


class FormDataGenerator:
    """Bla bla

    """
    def __init__(self,
                 form_template: str,
                 ):
        with open(FORM_DATA) as f:
            form_data_all = json.load(f)
        try:
            form_data = form_data_all[form_template]
        except KeyError:
            raise ValueError(f'Form template "{form_template}" not found in form data')

        self._extractor_agents = [
            _map_extractor_agents[cv_data_type] for cv_data_type in form_data['text_content_parts']
        ]
