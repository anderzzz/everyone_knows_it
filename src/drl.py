"""Data-retrieval layer for application.

"""
import os

path_to_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../abtDataStore')

_registry = {
    'george samsa': {
        'education': os.path.join(path_to_data_dir, 'george_samsa_education.json'),
        'employment': os.path.join(path_to_data_dir, 'george_samsa_employment.json'),
        'skills': os.path.join(path_to_data_dir, 'george_samsa_skills.json'),
        'publications': os.path.join(path_to_data_dir, 'george_samsa_publications.json')
    },
}


def get_data(person_name: str, data_type: str):
    """Get data for person by name and type of personal data.

    """
    try:
        person_bio = _registry[person_name]
        try:
            return person_bio[data_type]
        except KeyError:
            raise ValueError(f'Data type `"{data_type}"` not found for person `"{person_name}"`')
    except KeyError:
        raise ValueError(f'Data for person `"{person_name}"` not found in registry')
