"""Creation of HTML files based on formTemplatesStore and data

"""
import os
from typing import Sequence

from jinja2 import Environment, FileSystemLoader, BaseLoader, TemplateNotFound

from .cv_data import CVData
from .dao import FormTemplatesDAO


class CustomTemplateLoader(BaseLoader):
    def __init__(self, dao: FormTemplatesDAO):
        self.dao = dao

    def get_source(self, environment, template):
        try:
            source = self.dao.get(template)
        except KeyError:
            raise TemplateNotFound(template)
        template_path = self.dao.path(template)
        mtime = os.path.getmtime(template_path)
        return source, template_path, lambda: mtime

    def list_templates(self):
        return self.dao.keys()

    def is_up_to_date(self, environment, template):
        try:
            source, filename, uptodate = self.get_source(environment, template)
        except TemplateNotFound:
            return False
        return uptodate()


env = Environment(loader=CustomTemplateLoader(FormTemplatesDAO()))


def populate_html(
        template_name: str,
        cv_data: Sequence[CVData],
):
    """Construct the HTML file from the template and data

    """
    template = env.get_template(template_name)
    cv_data_objs = {cv_data_obj.__class__.__name__.lower(): cv_data_obj for cv_data_obj in cv_data}

    return template.render(**cv_data_objs)
