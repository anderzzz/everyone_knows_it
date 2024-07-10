"""Registry of tools that can be used by the agent.

"""
from .cv_data import (
    create_educations,
)

_tools = {
    'create_educations': create_educations,
}


def get_tool(name):
    """Get a tool by name

    """
    try:
        return _tools[name]
    except KeyError:
        raise ValueError(f'Tool "{name}" not found in registry')
