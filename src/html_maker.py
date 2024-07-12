"""Creation of HTML files based on formTemplatesStore and CV data objects

"""
import os
from typing import Sequence, Tuple, Callable

from jinja2 import Environment, BaseLoader, TemplateNotFound

from .cv_data import CVData
from .dao import FormTemplatesDAO


class CustomTemplateLoader(BaseLoader):
    """Custom template loader for the jinja form templates which are accessed via the DAO

    See: https://tedboy.github.io/jinja2/generated/generated/jinja2.BaseLoader.html

    """
    def __init__(self, dao: FormTemplatesDAO):
        self.dao = dao

    def get_source(self, environment, template) -> Tuple[str, str, Callable]:
        try:
            source = self.dao.get(template)
        except KeyError:
            raise TemplateNotFound(template)
        template_path = self.dao.path(template)
        mtime = os.path.getmtime(template_path)
        return source, template_path, lambda: mtime == os.path.getmtime(template_path)

    def list_templates(self):
        return self.dao.keys()


env = Environment(loader=CustomTemplateLoader(dao=FormTemplatesDAO()))


def populate_html(
        template_name: str,
        cv_data: Sequence[CVData],
):
    """Construct the HTML file from the template and data

    Note that this function require that the template variables are named after the CVData classes
    in lower case. For example, if the CVData class is `Educations`, then the template variable
    should be `educations`. Individual attributes of the CVData object can be accessed using the
    dot notation. For example, `educations[0].school` will access the `school` attribute of the
    first `Educations` object in the sequence.

    Args:
        template_name (str): Name of the template file
        cv_data (Sequence[CVData]): Sequence of CVData objects

    """
    template = env.get_template(template_name)
    cv_data_objs = {cv_data_obj.__class__.__name__.lower(): cv_data_obj for cv_data_obj in cv_data}

    return template.render(**cv_data_objs)
