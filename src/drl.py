"""Data-retrieval layer for application.

"""
import os

path_to_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../abtM3DataStore')

_registry = {
    'education': os.path.join(path_to_data_dir, 'education.json'),
    'employment': os.path.join(path_to_data_dir, 'employment.json'),
}


def get_data(name):
    """Get data by name

    """
    try:
        return _registry[name]
    except KeyError:
        raise ValueError(f'Data "{name}" not found in registry')
