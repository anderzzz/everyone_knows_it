"""Registry instances of personal data and job ads.

"""
import os


path_to_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../abtDataStore')
path_to_ad_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../jobAdsStore')


class Register:
    """A simple read-only registry class for file content.

    """
    def __init__(self, registry: dict):
        self.registry = registry

    def get(self, *keys) -> str:
        """Get value from registry by one or several keys.

        Args:
            *keys: str
                One or several keys to traverse the registry.

        Returns:
            The text data

        """
        if len(keys) == 0:
            raise ValueError('At least one key must be provided')

        value = self.registry
        try:
            for key in keys:
                value = value[key]
        except KeyError:
            raise ValueError(f'Error at key `"{key}"` in keys: {keys}. Check the registry.')

        with open(value, 'r') as f:
            return f.read()


register_persons = Register({
        'george samsa': {
            'education': os.path.join(path_to_data_dir, 'gregor_samsa_education.json'),
            'employment': os.path.join(path_to_data_dir, 'gregor_samsa_employment.json'),
            'skills': os.path.join(path_to_data_dir, 'gregor_samsa_skills.json'),
            'publications': os.path.join(path_to_data_dir, 'gregor_samsa_publications.json')
        }}
)
register_job_ads = Register({
        'epic_resolution_index': {
            'luxury_retail_lighting_specialist': os.path.join(path_to_ad_dir, 'epic_resolution_index.txt'),
        },
        'geworfenheit': {
            'urban entomology specialist': os.path.join(path_to_ad_dir, 'geworfenheit.txt'),
        }}
)
register_form_templates = Register({})
