"""Input data retrieval layer

"""
import json
import os

from .registry import Registry


path_to_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../abtDataStore')
path_to_ad_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../jobAdsStore')
path_to_form_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../formTemplatesStore')
path_to_form_toc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../formTemplatesStore/_form_templates_toc.json')

registry_persons = Registry({
    'gregor samsa': {
        'education': os.path.join(path_to_data_dir, 'gregor_samsa_education.json'),
        'employment': os.path.join(path_to_data_dir, 'gregor_samsa_employment.json'),
        'skills': os.path.join(path_to_data_dir, 'gregor_samsa_skills.json'),
        'publications': os.path.join(path_to_data_dir, 'gregor_samsa_publications.json')
    }},
    read=True
)
registry_job_ads = Registry({
    'epic resolution index': {
        'luxury retail lighting specialist': os.path.join(path_to_ad_dir, 'epic_resolution_index.txt'),
    },
    'geworfenheit': {
        'urban entomology specialist': os.path.join(path_to_ad_dir, 'geworfenheit.txt'),
    }},
    read=True
)
registry_form_templates = Registry({
    'two_columns_0': os.path.join(path_to_form_dir, 'two_columns_0.html'),
    },
    read=True
)
with open(path_to_form_toc, 'r') as f:
    registry_form_templates_toc = Registry(json.load(f), read=False)
