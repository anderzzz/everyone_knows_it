"""Registry instances of personal data and job ads.

"""
import os


path_to_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../abtDataStore')
path_to_ad_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../jobAdsStore')

_registry_persons = {
    'george samsa': {
        'education': os.path.join(path_to_data_dir, 'george_samsa_education.json'),
        'employment': os.path.join(path_to_data_dir, 'george_samsa_employment.json'),
        'skills': os.path.join(path_to_data_dir, 'george_samsa_skills.json'),
        'publications': os.path.join(path_to_data_dir, 'george_samsa_publications.json')
    },
}
_registry_job_ads = {
    'epic_resolution_index': {
        'luxury_retail_lighting_specialist': os.path.join(path_to_data_dir, 'epic_resolution_index.txt'),
    },
    'geworfenheit': {
        'urban entomology specialist': os.path.join(path_to_data_dir, 'geworfenheit.txt'),
    }
}
