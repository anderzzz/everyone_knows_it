"""Data-retrieval layer for application.

"""
from _registry import _registry_persons, _registry_job_ads


def get_personal_data(person_name: str, data_type: str):
    """Get data for person by name and type of personal data.

    """
    try:
        person_bio = _registry_persons[person_name]
        try:
            return person_bio[data_type]
        except KeyError:
            raise ValueError(f'Data type `"{data_type}"` not found for person `"{person_name}"`')
    except KeyError:
        raise ValueError(f'Data for person `"{person_name}"` not found in registry')


def get_job_ad(company: str, position: str):
    """Get job ad by company and position.

    """
    try:
        company_ads = _registry_job_ads[company]
        try:
            return company_ads[position]
        except KeyError:
            raise ValueError(f'Position `"{position}"` not found for company `"{company}"`')
    except KeyError:
        raise ValueError(f'Job ads for company `"{company}"` not found in registry')
