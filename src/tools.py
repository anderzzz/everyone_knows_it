"""Registry of tools that can be used by the agent.

"""
from cv_data import (
    create_educations,
)
from funcs import (
    is_url_live,
)

_tools = {
    'is_url_live': is_url_live,
    'create_educations': create_educations,
}


def get_tool(name):
    """Get a tool by name

    """
    try:
        return _tools[name]
    except KeyError:
        raise ValueError(f'Tool "{name}" not found in registry')
