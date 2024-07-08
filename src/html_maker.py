"""Creation of HTML files based on cv_templates and data

"""
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('cv_templates'))
template = env.get_template('test_template.html')

