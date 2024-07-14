"""Creation of prompts from templates

"""
import os
from jinja2 import Environment, FileSystemLoader

_prompt_templates_dir_name = 'prompt_templates'
env = Environment(
    loader=FileSystemLoader(
        searchpath=os.path.join(os.path.dirname(os.path.abspath(__file__)), _prompt_templates_dir_name)
    )
)


def get_prompt_for_(agent_type: str, **kwargs):
    """Construct the prompt from the template and data

    Note that the data to be inserted into the template is passed as keyword arguments
    where the key has to match the variable name in the template

    This also assumes the prompt templates is a text file named after the agent and with
    the extension '.txt'

    Args:
        agent_type (str): Type of the agent
        **kwargs: Data to be inserted into the template

    """
    return env.get_template(f'{agent_type}.txt').render(**kwargs)
