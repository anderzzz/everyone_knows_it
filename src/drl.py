"""Input data retrieval layer

"""
import json
import os

from .registry import Registry


path_to_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../abtDataStore')
path_to_ad_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../jobAdsStore')
path_to_form_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../formTemplatesStore')
path_to_form_toc = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'form_data_confs/_form_templates_toc.json')

registry_persons = Registry({
        'gregor samsa': {
            'education': os.path.join(path_to_data_dir, 'gregor_samsa_education.json'),
            'employment': os.path.join(path_to_data_dir, 'gregor_samsa_employment.json'),
            'skills': os.path.join(path_to_data_dir, 'gregor_samsa_skills.json'),
            'publications': os.path.join(path_to_data_dir, 'gregor_samsa_publications.json')
        }}
)
registry_job_ads = Registry({
        'epic resolution index': {
            'luxury retail lighting specialist': os.path.join(path_to_ad_dir, 'epic_resolution_index.txt'),
        },
        'geworfenheit': {
            'urban entomology specialist': os.path.join(path_to_ad_dir, 'geworfenheit.txt'),
        }}
)
registry_form_templates = Registry({
    'two_columns_0': os.path.join(path_to_form_dir, 'two_columns_0.html'),
})

def get_required_cv_data_types_for_(form_template: str) -> list:
    """Get the required data types for a CV template

    Args:
        form_template: The form template to get the required data types for

    Returns:
        The required data types for the CV template

    """
    HERE
    return ['education', 'employment', 'skills', 'publications']

