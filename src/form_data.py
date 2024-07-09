"""

"""
import json

from .consts import FORM_DATA
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


def get_extractor_agents_for_(form_template: str):
    with open(FORM_DATA) as f:
        form_data_all = json.load(f)
    try:
        form_data = form_data_all[form_template]
    except KeyError:
        raise ValueError(f'Form template "{form_template}" not found in form data')

    return [
        _map_extractor_agents[cv_data_type] for cv_data_type in form_data['text_content_parts']
    ]
