"""Registry of tools that can be used by the agent.

"""
from .registry import Registry
from .cv_data import (
    Educations,
    Employments,
    Skills,
    Biography,
)

registry_tool_funcs = Registry({
    'create_educations': Educations.build,
    'create_employments': Employments.build,
    'create_skills': Skills.build,
    'create_biography': Biography.build
}, read=False)
