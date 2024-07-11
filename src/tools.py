"""Registry of tools that can be used by the agent.

"""
from .registry import Registry
from .cv_data import (
    create_educations,
    create_employments,
    create_skills,
    create_biography,
)

registry_tool_funcs = Registry({
    'create_educations': create_educations,
    'create_employments': create_employments,
    'create_skills': create_skills,
    'create_biography': create_biography,
}, read=False)
