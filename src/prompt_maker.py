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


def get_prompt_for_(agent_name: str, **kwargs):
    return env.get_template(f'{agent_name}.txt').render(**kwargs)
